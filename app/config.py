import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))  # Adjust path if needed

default_db_loc = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SQLALCHEMY_DATABASE_URI = default_db_loc
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-hardcoded-secret')
