from flask import render_template, request, redirect, url_for, session, flash
from app.models import User, db, ActivityRegistry, SharedActivity
from datetime import datetime, timedelta, date
from flask_login import login_user, logout_user, login_required, current_user
import io, csv

from app.services.activity_service import (
    get_shared_activities_with_user,
    get_user_activities,
    get_latest_activity_entry,
    get_weekly_calories_summary,
    get_global_leaderboard,
    get_shared_activity_summary_by_type
)

# from app import db  # Uncomment if using database
def calculate_calories(activity, duration, weight):
    met_values = {
        "walking": 3.5,
        "running": 8.3,
        "cycling": 6.0,
        "hiking": 6.0,
        "swimming": 5.8,
        "yoga": 2.5
    }
    
    return round(duration * met_values[activity] * weight * 0.0175, 2)

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
        ).order_by(ActivityRegistry.activity_date.asc()).all()


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
            timedelta=timedelta,
            start=start,
            end=end
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
            # ===== CSV Upload =====
            if 'csv_files' in request.files:
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
                                    trail_name=row.get('trail_name')  # <== 新增支援 trail_name
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

            # ===== Manual or Trail form =====
            else:
                try:
                    activity = request.form['activity'].lower()
                    duration = float(request.form['duration'])
                    weight = float(request.form['weight'])

                    met_values = {
                        "walking": 3.5, "running": 8.3, "cycling": 6.0,
                        "hiking": 6.0, "swimming": 5.8, "yoga": 2.5
                    }

                    met = met_values.get(activity, 3.5)
                    calories_burned = round(duration * met * weight * 0.0175, 2)
                    activity_length = (datetime.min + timedelta(minutes=duration)).time()

                    distance_m = request.form.get('distance_m') or None
                    trail_name = request.form.get('trail_name') or None  # <== 新增支援 trail_name

                    new_entry = ActivityRegistry(
                        upload_user_id=current_user.id,
                        upload_time=datetime.now(),
                        activity_date=datetime.today().date(),
                        activity_type=activity,
                        activity_length=activity_length,
                        calories_burned=calories_burned,
                        weight_kg=weight,
                        distance_m=float(distance_m) if distance_m else None,
                        trail_name=trail_name  # <== 寫入資料庫
                    )

                    db.session.add(new_entry)
                    db.session.commit()

                    # 傳遞給 dashboard 使用
                    session['calories_burned'] = calories_burned
                    session['selected_activity'] = activity.title()
                    session['duration'] = duration

                    return redirect(url_for('dashboard'))

                except Exception as e:
                    flash(f"Failed to save entry: {e}", "error")
                    return redirect(url_for('calories'))

        # ===== GET request =====
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
        confirm_password = request.form.get('confirmPassword')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('index'))


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
        limit = request.args.get("limit", default=10, type=int)
        page = request.args.get("page", default=1, type=int)

        all_shared = get_shared_activities_with_user(current_user.email)
        all_shared_sorted = sorted(
            all_shared,
            key=lambda x: (x["activity_date"], x["upload_time"]),
            reverse=True
        )                                                   

        total_items = len(all_shared_sorted)
        start = (page - 1) * limit
        end = start + limit
        shared_data = all_shared_sorted[start:end]

        leaderboard = get_global_leaderboard()
        shared_summary = get_shared_activity_summary_by_type(current_user.email)

        return render_template(
            "shared_with_me.html",
            shared_data=shared_data,
            leaderboard=leaderboard,
            shared_summary=shared_summary,
            limit=limit,
            page=page,
            total_items=total_items
        )


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

        # GET: Pagination
        limit = request.args.get("limit", default=10, type=int)
        page = request.args.get("page", default=1, type=int)
        offset = (page - 1) * limit

        query = ActivityRegistry.query \
            .filter_by(upload_user_id=current_user.id) \
            .order_by(ActivityRegistry.activity_date.desc(),
                      ActivityRegistry.upload_time.desc()
                      )

        total_items = query.count()
        activities = query.offset(offset).limit(limit).all()


        # return render_template("share.html", activities=activities)
        return render_template("share.html", activities=activities, limit=limit, page=page, total_items=total_items)



    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('index'))


