from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import random
import unittest
from random_username.generate import generate_username
from app.config import TestingConfig

def addUser(name, email, password_hash):
    to_add = User(username=name, email = email, password_hash = password_hash)
    db.session.add(to_add)

class UnitTestingHandler(unittest.TestCase):
    def test_setup(self):
        testValue = True
        try:
            self.app = create_app(TestingConfig)
            print("App Setup Test Suceeded.")
        except Exception as e:
            testValue = False
            print("App Setup Test Failed")
            print(f"Error Message: {e}")
        return testValue

class TestDBcreation():
    def __init__(self, handler):
        self.handler = handler
        
    def test_user_addition(self):
        testValue = True
        try:
            with self.handler.app.app_context():
                db.create_all()
                print("DB Setup Test Suceeded")
        except Exception as e:
            testValue = False
            print("DB Setup Test Failed")
            print(f"Error Message: {e}")
        return testValue

class TestDBAddition():
    def __init__(self, handler):
        self.handler = handler
        
    def test_db_addition(self, count): 
        testValue = True
        self.handler.users_to_add = generate_username(count)
        self.handler.user_password_dictionary = {}
        with self.handler.app.app_context():
            try:
                for user in self.handler.users_to_add:
                    password = list(user)
                    random.shuffle(password)
                    password = "".join(password) # Shuffles the username randomly to generate a password.
                    addUser(user, user + "@mail.com", password_hash=generate_password_hash(password))
                    self.handler.user_password_dictionary[user] = password

                added_users = db.session.query(User).all()
                if len(added_users) == len(self.handler.users_to_add):
                    print(f"Database Randomized Addition Test Succeeded with {count} random users. ")
                else:
                    print(f"Database Randomized Addition Test Failed, database is missing {len(self.handler.users_to_add) - len(added_users)} users")
            except Exception as e:
                print("DB Randomized Addition Test Failed")
                print(f"Error Message: {e}")
        return testValue

testing_handler = UnitTestingHandler()
testing_handler.test_setup()
TestDBcreation(testing_handler).test_user_addition()
TestDBAddition(testing_handler).test_db_addition(10)