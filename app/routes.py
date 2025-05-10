from flask import render_template, request, redirect, url_for, session
from flask import request, redirect, url_for, session, flash
from app.models import User, db, ActivityRegistry
from datetime import datetime, timedelta
from flask_login import login_user, logout_user, login_required, current_user



# from app import db  # Uncomment if using database

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
                met = met_values[activity]
                calories_burned = round(duration * met * weight * 0.0175, 2)

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
            # session['user_id'] = user.user_id
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


    @app.route('/logout')
    def logout():
        # session.clear()
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('index'))


