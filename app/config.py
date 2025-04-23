import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_db_loc = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASEURL') or default_db_loc
    SECRET_KEY = '????'
    