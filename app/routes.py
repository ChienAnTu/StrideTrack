from flask import render_template, request, redirect, url_for, session
from flask import request, redirect, url_for, session, flash
from app.models import User, db, ActivityRegistry, SharedActivity
from datetime import datetime, timedelta
from flask_login import login_user, logout_user, login_required, current_user

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
        calories_burned = session.get('calories_burned')
        selected_activity = session.get('selected_activity')
        duration = session.get('duration')

        return render_template(
            'dashboard.html',
            title="Dashboard",
            user=current_user,
            calories=calories_burned,
            activity=selected_activity,
            duration=duration
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
        calories_burned = None
        if request.method == 'POST':
            activity = request.form['activity'].lower()
            duration = float(request.form['duration'])
            weight = float(request.form['weight'])

            met_values = {
                "walking": 3.5,
                "running": 8.3,
                "cycling": 6.0,
                "hiking": 6.0,
                "swimming": 5.8,
                "yoga": 2.5
            }

            if activity in met_values:
                calories_burned = calculate_calories(activity, duration, weight)
                # Save to session
                session['calories_burned'] = calories_burned
                session['selected_activity'] = activity.title()
                session['duration'] = duration

                # Insert into ActivityRegistry
                try:
                    # user_id = session.get('user_id', 1)  # use actual user ID if available
                    user_id = current_user.id
                    now = datetime.now()
                    activity_length = (datetime.min + timedelta(minutes=duration)).time()

                    new_entry = ActivityRegistry(
                        upload_user_id=user_id,
                        upload_time=now,
                        activity_date=now.date(),
                        activity_type=activity,
                        activity_length=activity_length,
                        calories_burned=calories_burned 
                    )

                    db.session.add(new_entry)
                    db.session.commit()
                except Exception as e:
                    print("Activity insert failed:", e)

                return redirect(url_for('dashboard'))

        return render_template(
            'calories.html',
            title="Calorie Calculator",
            calories=calories_burned,
            # user={'username': 'Guest'}
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
        records = ActivityRegistry.query.filter_by(upload_user_id=current_user.id).all()

        activities = [
            {
                "activity_type": r.activity_type,
                "activity_length": str(r.activity_length),
                "activity_date": r.activity_date.strftime('%Y-%m-%d'),
                "calories_burned": r.calories_burned  # ✅ This is needed!
            }
            for r in records
        ]

        return render_template("visualise.html", activities=activities)

    # -------------Share data view--------------
    @app.route('/shared_with_me')
    @login_required
    def shared_with_me():
        # Finds out data shared with current user
        shares = SharedActivity.query.filter_by(user_shared_with=current_user.email).all()

        shared_data = []
        for share in shares:
            # Findes out activities shared
            activity = ActivityRegistry.query.filter_by(
                upload_user_id=share.sharing_user,
                upload_time=share.activity_upload_time
            ).first()

            # Finds out the email of whom shares the data
            sharing_user = User.query.get(share.sharing_user)

            if activity and sharing_user:
                shared_data.append({
                    "activity_type": activity.activity_type.title(),
                    "activity_length": activity.activity_length,
                    "activity_date": activity.activity_date.strftime('%Y-%m-%d'),
                    "calories_burned": activity.calories_burned,
                    "shared_by": sharing_user.email
                })

        return render_template("shared_with_me.html", shared_data=shared_data)

    @app.route('/share', methods=['GET', 'POST'])
    @login_required
    def share():
        if request.method == 'POST':
            share_email = request.form.get('share_email')
            # upload_time = request.form.get('upload_time')
            upload_time_str = request.form.get('upload_time')
            upload_time = datetime.fromisoformat(upload_time_str)

            # Check if the email exists
            target_user = User.query.filter_by(email=share_email).first()
            if not target_user:
                flash("The user you're trying to share with does not exist.")
                return redirect(url_for('share'))

            new_share = SharedActivity(
                sharing_user=current_user.id,
                activity_upload_time=upload_time,
                user_shared_with=share_email
            )

            try:
                db.session.add(new_share)
                db.session.commit()
                flash("Activity shared successfully.")
            except Exception as e:
                print("Share failed:", e)
                flash("An error occurred while sharing.")

            return redirect(url_for('share'))

        # GET request
        activities = ActivityRegistry.query.filter_by(upload_user_id=current_user.id).all()
        return render_template("share.html", activities=activities)



    @app.route('/logout')
    def logout():
        # session.clear()
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('index'))


