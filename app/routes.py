from flask import render_template
from app import db
from app.__init__ import create_app

application = create_app()

@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html')

@application.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
