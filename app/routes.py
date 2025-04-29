from flask import render_template
# from app import db  # Uncomment if using database

def register_routes(app):
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

