from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import random
import unittest
from random_username.generate import generate_username
from app.config import TestingConfig

def addUser(name, email, password_hash):
    to_add = User(username=name, email = email, password_hash = password_hash)
    db.session.add(to_add)
    db.session.commit()

class UnitTestingHandler(unittest.TestCase):
    def test_setup(self):
        testValue = True
        try:
            self.app = create_app(TestingConfig)
            with self.app.app_context():
                db.drop_all() # Wipe the testing database clean for new additions.
            print("App Setup Test passed")
        except Exception as e:
            testValue = False
            print("App Setup Test failed")
            print(f"Error Message: {e}")
        return testValue

class DatabaseTestHandler():
    def __init__(self, handler):
        self.handler = handler
        
    def test_database_creation(self):
        testValue = True
        try:
            with self.handler.app.app_context():
                db.create_all()
                print("DB Setup Test passed")
        except Exception as e:
            testValue = False
            print("DB Setup Test failed")
            print(f"Error Message: {e}")
        return testValue
        
    def test_db_addition(self, count): 
        testValue = True
        self.handler.test_users = generate_username(count)
        self.handler.user_password_dictionary = {}
        self.handler.user_passwordHash_dictionary = {}
        with self.handler.app.app_context():
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
        with self.handler.app.app_context():
            for user in self.handler.test_users:
                if (check_password_hash(self.handler.user_passwordHash_dictionary[user], self.handler.user_password_dictionary[user])
                    ) == False:
                    print(f"Hash testing for user {user} failed! Hashed password is not recognized")
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
            

testing_handler = UnitTestingHandler()
testing_handler.test_setup()
database_test_handler = DatabaseTestHandler(testing_handler)
database_test_handler.test_database_creation()
database_test_handler.test_db_addition(100)
database_test_handler.test_password_hashing()
database_test_handler.test_user_ID()