from flask import render_template, request, redirect, url_for, session, flash

# from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import RegistrationForm, LoginForm
from app.database import db


def register_routes(app):
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        calories_burned = session.get('calories_burned')
        selected_activity = session.get('selected_activity')
        duration = session.get('duration')

        return render_template(
            'dashboard.html',
            title="Dashboard",
            user={'username': 'User'},
            calories=calories_burned,
            activity=selected_activity,
            duration=duration
        )


    # === Register route ===
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))  # Re-direct if already logged in

        form = RegistrationForm()
        if form.validate_on_submit():
            # Set the user attributes from the form data
            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()
            flash("Account created successfully! You can now log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html", form=form)


    # === Login route ===
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid email or password.", "danger")

        return render_template("login.html", form=form)

    # === Logout route ===
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))


    @app.route('/calories', methods=['GET', 'POST'])
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
                session['calories_burned'] = calories_burned
                session['selected_activity'] = activity.title()  # Save capitalized activity
                session['duration'] = duration  

                return redirect(url_for('dashboard'))

        return render_template(
            'calories.html',
            title="Calorie Calculator",
            calories=calories_burned,
            user={'username': 'Guest'}
        )

