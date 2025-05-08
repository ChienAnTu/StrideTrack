from flask import render_template, request, redirect, url_for, session

# from app import db  # Uncomment if using database

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

