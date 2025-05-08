import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_db_loc = 'sqlite:///' + os.path.join(basedir, 'app.db')  
print(default_db_loc)


class Config:
    SQLALCHEMY_DATABASE_URI = default_db_loc
    SECRET_KEY = os.urandom(10)