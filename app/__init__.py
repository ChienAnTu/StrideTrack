from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application,db)

from app import models

@application.route('/')
def index():
    return render_template('index.html')

if __name__== '__main__':
    application.run()