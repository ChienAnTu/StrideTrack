from flask import Flask, g, session
# Import backend modules below
from app.database import db, migrate
from app.models import User
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config
from datetime import datetime
# from sqlalchemy.orm import DeclarativeBase

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # --- Setup Flask-Login ---
    login_manager = LoginManager()
    login_manager.login_view = 'index'  # Redirect to 'index' if not logged in
    login_manager.login_message = "Please log in to access this page."
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # -----------------------------------

    app.jinja_env.filters['todatetime'] = lambda s: datetime.strptime(s, "%Y-%m-%d")

    # Register routes
    from app.routes import register_routes
    register_routes(app)

    from app import models  # Ensure models are imported
    return app

def create_testing_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # --- Setup Flask-Login ---
    login_manager = LoginManager()
    login_manager.login_view = 'index'  # Redirect to 'index' if not logged in
    login_manager.login_message = "Please log in to access this page."
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # -----------------------------------

    # Register routes
    from app.routes import register_routes
    register_routes(app)

    from app import models  # Ensure models are imported
    return app






