from app import create_testing_app, db
from app.models import User, ActivityRegistry
from datetime import date, time, datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random
import unittest
import multiprocessing
import threading
from selenium import webdriver
from random_username.generate import generate_username
from app.config import TestingConfig
from app.routes import calculate_calories

LOCALHOST = "http://localhost:5000/"

ACTIVITY_MET_VALUES = {
    "walking": 3.5,
    "running": 8.3,
    "cycling": 6.0,
    "hiking": 6.0,
    "swimming": 5.8,
    "yoga": 2.5
}

ACTIVITY_TYPES = {
    1 : "walking",
    2 : "running",
    3 : "cycling",
    4 : "hiking",
    5 : "swimming",
    6 : "yoga"
}

def addUser(name, email, password_hash):
    to_add = User(username=name, email = email, password_hash = password_hash)
    db.session.add(to_add)
    db.session.commit()

def addActivity(upload_user_id, activity_type, activity_date, activity_length):
    to_add = ActivityRegistry (
        upload_user_id = upload_user_id, 
        upload_time = datetime.datetime.now(),
        activity_date = activity_date,
        activity_length = activity_length
        )
    db.session.add(to_add)
    db.session.commit()

def create_test_server():
    """Creates and runs the Flask test server."""
    app = create_testing_app(TestingConfig)
    app.run()

class UnitTestingHandler(unittest.TestCase):
    def test_setup(self):
        testValue = True
        try:
            self.app = create_testing_app(TestingConfig)
            self.app_context = self.app.app_context()
            self.app_context.push()
            with self.app_context:
                db.drop_all()  # Wipe the testing database clean for new additions.
            print("App Setup Test passed")
        except Exception as e:
            testValue = False
            print("App Setup Test failed")
            print(f"Error Message: {e}")
        return testValue
        
class SeleniumTestHandler():
    def __init__(self, parent):
        self.parent = parent
        parent.server_thread = multiprocessing.Process(target=create_test_server)
        parent.driver = webdriver.Chrome()
    
    def setup_test_server(self):
        self.parent.server_thread.start()
        self.parent.driver.get(LOCALHOST)

class DatabaseTestHandler():
    def __init__(self, parent):
        self.handler = parent
        
    def test_database_creation(self):
        testValue = True
        try:
            with self.handler.app_context:
                db.create_all()
                print("DB Setup Test passed")
        except Exception as e:
            testValue = False
            print("DB Setup Test failed")
            print(f"Error Message: {e}")
        return testValue
        
    def test_db_user_addition(self, count):
        testValue = True
        self.handler.test_users = generate_username(count)
        self.handler.user_password_dictionary = {}
        self.handler.user_passwordHash_dictionary = {}
        with self.handler.app_context:
            try:
                for user in self.handler.test_users:
                    password = list(user)
                    random.shuffle(password)
                    password = "".join(password) # Shuffles the username randomly to generate a password.
                    password_hash = generate_password_hash(password)
                    addUser(user, user + "@mail.com", password_hash=password_hash)
                    self.handler.user_password_dictionary[user] = password
                    self.handler.user_passwordHash_dictionary[user] = password_hash

                added_users = db.session.query(User).all()
                if len(added_users) == len(self.handler.test_users):
                    print(f"Database Randomized Addition Test passed with {count} random users. ")
                    self.handler.users_in_db = added_users
                else:
                    print(f"Database Randomized Addition Test failed, database is missing {len(self.handler.users_to_add) - len(added_users)} users")
                    testValue = False
            except Exception as e:
                testValue = False
                print("DB Randomized Addition Test failed")
                print(f"Error Message: {e}")
        return testValue
    
    def test_password_hashing(self):
        testValue = True
        with self.handler.app_context:
            for user in self.handler.test_users:
                if (check_password_hash(self.handler.user_passwordHash_dictionary[user], self.handler.user_password_dictionary[user])
                    ) == False:
                    print(f"Hash testing for user {user} failed! User password is not recognized by the database!")
                    testValue = False
            if testValue == True:
                print("Password Hashing Testing passed")
                
    def test_user_ID(self):
        testValue = True
        counter = 1
        for user in self.handler.users_in_db:
            if user.id != counter:
                testValue=False
                print(f"User ID auto-increment testing failed at user_ID: {user.id}, expected: {counter}")
            counter += 1
        print("User ID auto-increment testing passed")
        return testValue
        
if __name__ == '__main__':
    testing_handler = UnitTestingHandler()
    testing_handler.test_setup()
    database_test_handler = DatabaseTestHandler(testing_handler)
    selenium_test_handler = SeleniumTestHandler(testing_handler)
    database_test_handler.test_database_creation()
    database_test_handler.test_db_user_addition(20)
    database_test_handler.test_password_hashing()
    database_test_handler.test_user_ID()
    selenium_test_handler.setup_test_server()
    