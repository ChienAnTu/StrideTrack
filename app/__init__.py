from flask import Flask, g, session
# Import backend modules below
from app.config import Config
from app.database import db, migrate
from app.models import User
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Middleware to set user in global context
    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = User.query.get(user_id)

    # ----Attach database to app here----
    db.init_app(app)
    migrate.init_app(app, db)
    # -----------------------------------

    # Register routes here
    from app.routes import register_routes
    register_routes(app)

    from app import models  # Ensure models are imported
    return app



