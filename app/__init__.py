from flask import Flask
# Import backend modules below
from app.config import Config
from app.database import db, migrate
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ----Attach database to app here----
    db.init_app(app)
    migrate.init_app(app, db)
    # -----------------------------------

    # Register routes here
    from app.routes import register_routes
    register_routes(app)

    from app import models  # Ensure models are imported
    return app
    


