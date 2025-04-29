from flask import Flask
# Import backend modules below
from app.config import Config
from app.database import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ----Attach database to app here----
    db.init_app(app)
    migrate.init_app(app, db)
    # -----------------------------------

    from app import routes

    return app


