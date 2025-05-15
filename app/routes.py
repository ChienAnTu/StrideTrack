from flask import render_template, request, redirect, url_for, session, flash
from app.models import User, db, ActivityRegistry, SharedActivity
from datetime import datetime, timedelta, date
from flask_login import login_user, logout_user, login_required, current_user
import io, csv

from app.services.activity_service import (
    get_shared_activities_with_user,
    get_user_activities,
    get_latest_activity_entry,
    get_weekly_calories_summary
)


def register_routes(app):
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')


    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Get optional GET params
        week_start_str = request.args.get('week_start')
        goal_str = request.args.get('goal')
        range_type = request.args.get('range', 'weekly')  # default to 'weekly'

        # Determine current day
        today = date.today()

        # Determine the date range for activity filtering
        if range_type == 'daily':
            start = end = today
        elif range_type == 'monthly':
            start = today.replace(day=1)
            # Set end to last day of the current month
            if start.month == 12:
                end = date(start.year + 1, 1, 1) - timedelta(days=1)
            else:
                end = date(start.year, start.month + 1, 1) - timedelta(days=1)
        else:  # weekly default
            if week_start_str:
                try:
                    start = datetime.strptime(week_start_str, "%Y-%m-%d").date()
                except ValueError:
                    start = today - timedelta(days=today.weekday())
            else:
                start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)

        # Filtered activities (for bar chart)
        activities = ActivityRegistry.query.filter(
            ActivityRegistry.upload_user_id == current_user.id,
            ActivityRegistry.activity_date.between(start, end)
        ).all()

        activities_data = [
            {
                "activity_type": a.activity_type,
                "activity_length": str(a.activity_length),
                "activity_date": a.activity_date.strftime('%Y-%m-%d'),
                "calories_burned": a.calories_burned
            }
            for a in activities
        ]

        # Weekly summary used for donut + line chart (always based on week_start)
        weekly_summary_start = start if range_type == 'weekly' else today - timedelta(days=today.weekday())
        goal = int(goal_str) if goal_str and goal_str.isdigit() else 300
        weekly = get_weekly_calories_summary(current_user.id, weekly_summary_start, goal)

        latest = get_latest_activity_entry(current_user.id)

        return render_template(
            'dashboard.html',
            title="Dashboard",
            user=current_user,
            calories=latest["calories"],
            activity=latest["activity"],
            duration=latest["duration"],
            activities=activities_data,
            weekly=weekly,
            timedelta=timedelta
        )

    @app.route('/challenges')
    def challenges():
        return render_template(
            'challenges.html',
            title="Challenges",
            user={'username': 'User'}
        )

    @app.route('/calories', methods=['GET', 'POST'])
    @login_required
    def calories():
        if request.method == 'POST':
            # Check if the POST is csv_file or manual
            if 'csv_files' in request.files:
                # ---------- CSV Upload Logic ----------
                uploaded_files = request.files.getlist("csv_files")
                total_success, total_failed = 0, 0

                for file in uploaded_files:
                    if not file or not file.filename.endswith('.csv'):
                        flash(f'Skipped invalid file: {file.filename}', 'error')
                        continue

                    try:
                        content = file.read().decode('utf-8')
                        reader = csv.DictReader(io.StringIO(content))

                        for row in reader:
                            try:                                
                                activity_date = datetime.strptime(row['activity_date'], '%d/%m/%Y').date()
                                duration_minutes = float(row['duration_minutes'])
                                activity_length = (datetime.min + timedelta(minutes=duration_minutes)).time()
                                weight = float(row['weight_kg']) if row.get('weight_kg') else 0
                                calories_burned = float(row['calories_burned']) if row.get('calories_burned') else \
                                    round(duration_minutes * weight * 0.0175 * 3.5, 2)

                                new_entry = ActivityRegistry(
                                    upload_user_id=current_user.id,
                                    upload_time=datetime.now(),
                                    activity_date=activity_date,
                                    activity_type=row['activity_type'],
                                    activity_length=activity_length,
                                    calories_burned=calories_burned,
                                    distance_m=float(row['distance_m']) if row.get('distance_m') else None,
                                    weight_kg=weight,
                                    # TODO: Delete below useless column
                                    average_speed_mps=float(row['average_speed_mps']) if row.get('average_speed_mps') else None,
                                    max_speed_mps=float(row['max_speed_mps']) if row.get('max_speed_mps') else None,
                                    start_lat=row.get('start_lat'),
                                    end_lat=row.get('end_lat')
                                )

                                db.session.add(new_entry)
                                total_success += 1
                            except Exception as e:
                                print(f"Row skipped: {e}")
                                total_failed += 1

                        db.session.commit()

                    except Exception as e:
                        print(f"Failed to process {file.filename}: {e}")
                        total_failed += 1

                flash(f"Uploaded {total_success} rows. Failed: {total_failed}", "info")
                return redirect(url_for('calories'))

            else:
                try:
            # ---------- Manual Form Entry ----------
                    # Required columns
                    activity = request.form['activity'].lower()
                    duration = float(request.form['duration'])
                    weight = float(request.form['weight'])

                    # factors
                    met_values = {
                        "walking": 3.5, "running": 8.3, "cycling": 6.0,
                        "hiking": 6.0, "swimming": 5.8, "yoga": 2.5
                    }

                    met = met_values.get(activity, 3.5)  # fallback: walking
                    calories_burned = round(duration * met * weight * 0.0175, 2)
                    activity_length = (datetime.min + timedelta(minutes=duration)).time()

                    # Nullable columns
                    distance_m = request.form.get('distance_m') or None
                    # average_speed_mps = request.form.get('average_speed_mps') or None
                    # max_speed_mps = request.form.get('max_speed_mps') or None
                    # start_lat = request.form.get('start_lat') or None
                    # end_lat = request.form.get('end_lat') or None

                    new_entry = ActivityRegistry(
                        upload_user_id=current_user.id,
                        upload_time=datetime.now(),
                        activity_date=datetime.today().date(),
                        activity_type=activity,
                        activity_length=activity_length,
                        calories_burned=calories_burned,
                        weight_kg=weight,
                        distance_m=float(distance_m) if distance_m else None
                        # average_speed_mps=float(average_speed_mps) if average_speed_mps else None,
                        # max_speed_mps=float(max_speed_mps) if max_speed_mps else None,
                        # start_lat=start_lat,
                        # end_lat=end_lat
                    )

                    db.session.add(new_entry)
                    db.session.commit()

                    # Data showed on dashboard TODO: -> modify here
                    session['calories_burned'] = calories_burned
                    session['selected_activity'] = activity.title()
                    session['duration'] = duration

                    return redirect(url_for('dashboard'))

                except Exception as e:
                    flash(f"Failed to save entry: {e}", "error")
                    return redirect(url_for('calories'))

        return render_template(
            'calories.html',
            title="Calorie Calculator",
            calories=session.get('calories_burned'),
            activity=session.get('selected_activity'),
            duration=session.get('duration'),
            user=current_user
        )
    
    @app.route('/register', methods=['POST'])
    def register():
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('index'))

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('index'))

    @app.route('/login', methods=['POST'])
    def login():
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # session['username'] = user.username
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.')
            return redirect(url_for('index'))
        
    @app.route('/visualise')
    @login_required
    def visualise():
        day_str = request.args.get('day')
        week_str = request.args.get('week')

        activities = get_user_activities(current_user.id)

        if day_str:
            try:
                selected_day = datetime.strptime(day_str, "%Y-%m-%d").date()
                activities = [a for a in activities if a["activity_date"] == selected_day.strftime("%Y-%m-%d")]
            except:
                flash("Invalid date format", "error")

        elif week_str:
            try:
                year, week_num = map(int, week_str.split("-W"))
                week_start = datetime.strptime(f'{year}-W{week_num}-1', "%Y-W%W-%w").date()
                week_end = week_start + timedelta(days=6)

                activities = [
                    a for a in activities
                    if week_start.strftime("%Y-%m-%d") <= a["activity_date"] <= week_end.strftime("%Y-%m-%d")
                ]
            except:
                flash("Invalid week format", "error")

        return render_template("visualise.html", activities=activities)


   
    # -------------Share data view--------------
    @app.route('/shared_with_me')
    @login_required
    def shared_with_me():
        shared_data = get_shared_activities_with_user(current_user.email)
        return render_template("shared_with_me.html", shared_data=shared_data)


    @app.route('/share', methods=['GET', 'POST'])
    @login_required
    def share():
        if request.method == 'POST':
            action = request.form.get('action')

            # Batch delete
            if action == 'delete':
                ids_to_delete = request.form.getlist('selected_ids')
                try:
                    for activity_id in ids_to_delete:
                        record = ActivityRegistry.query.filter_by(
                            upload_user_id=current_user.id,
                            id=int(activity_id)
                        ).first()
                        if record:
                            db.session.delete(record)

                    db.session.commit()
                    flash(f"Deleted {len(ids_to_delete)} activity record(s).", "info")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error deleting records: {e}", "error")

                return redirect(url_for('share'))

            # Batch share
            elif action == 'share':
                ids_str = request.form.get('share_ids', '')
                email = request.form.get('share_email', '').strip()

                if not email:
                    flash("No email provided for sharing.", "error")
                    return redirect(url_for('share'))

                share_ids = [int(i) for i in ids_str.split(',') if i.strip().isdigit()]

                try:
                    target_user = User.query.filter_by(email=email).first()
                    if not target_user:
                        flash("The user you're trying to share with does not exist.", "error")
                        return redirect(url_for('share'))

                    for activity_id in share_ids:
                        existing = SharedActivity.query.filter_by(
                            activity_id=activity_id,
                            user_shared_with=email
                        ).first()

                        if not existing:
                            new_share = SharedActivity(
                                activity_id=activity_id,
                                user_shared_with=email,
                                sharing_user_id=current_user.id
                            )
                            db.session.add(new_share)

                    db.session.commit()
                    flash(f"Shared {len(share_ids)} activity record(s) with {email}.", "info")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Failed to share: {e}", "error")

                return redirect(url_for('share'))

        # GET: Show limited list: support {?limit=10 or 20}
        limit = request.args.get("limit", default=10, type=int)
        activities = ActivityRegistry.query \
            .filter_by(upload_user_id=current_user.id) \
            .order_by(ActivityRegistry.activity_date.desc()) \
            .limit(limit).all()

        return render_template("share.html", activities=activities)


    @app.route('/logout')
    def logout():
        # session.clear()
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('index'))


