from flask import render_template, request, redirect, url_for, session, flash, jsonify

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
    @login_required
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
    @app.route("/register", methods=["POST"])
    def register():
        if current_user.is_authenticated:
            return jsonify({"success": False, "redirect": url_for("dashboard")})

        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        if not all([email, password, confirm_password, first_name, last_name]):
            return jsonify({"success": False, "error": "All fields are required."})

        if password != confirm_password:
            return jsonify({"success": False, "error": "Passwords do not match."})

        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "error": "Email already registered."})

        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"success": True, "message": "Registration successful."})


    # === Login route ===
    @app.route("/login", methods=["POST"])
    def login():
        if current_user.is_authenticated:
            return jsonify({"success": True, "redirect": url_for("dashboard")})

        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        remember = data.get("remember", False)

        if not email or not password:
            return jsonify({"success": False, "error": "Email and password required."})

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            return jsonify({"success": True, "redirect": url_for("dashboard")})
        else:
            return jsonify({"success": False, "error": "Invalid email or password."})


    # === Logout route ===
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        # flash("You have been logged out.", "info")
        return redirect(url_for("index", logout=1))


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

