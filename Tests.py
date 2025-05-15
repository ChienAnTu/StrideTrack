from app import create_testing_app, db
from app.models import User, ActivityRegistry
from datetime import date, time, datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
import unittest
import multiprocessing
import time as t_lib
from selenium import webdriver
from selenium.webdriver.common.by import By
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

def addActivity(upload_user_id, activity_type, activity_date, activity_length_minutes, weight_kg=None, distance_m=None, trail_name=None):
    from app.routes import calculate_calories
    
    # Convert minutes to time object
    activity_length = (datetime.min + timedelta(minutes=activity_length_minutes)).time()
    
    # Default weight if not provided
    weight = weight_kg if weight_kg is not None else 70.0
    calories_burned = calculate_calories(activity_type, activity_length_minutes, weight)

    to_add = ActivityRegistry(
        upload_user_id=upload_user_id,
        upload_time=datetime.now(),
        activity_date=activity_date,
        activity_type=activity_type,
        activity_length=activity_length,
        calories_burned=calories_burned,
        distance_m=distance_m,
        weight_kg=weight_kg,
        trail_name=trail_name
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
    
    def setup_test_server(self):
        self.parent.server_thread = multiprocessing.Process(target=create_test_server)
        self.parent.driver = webdriver.Chrome()
        self.parent.server_thread.start()
        self.parent.driver.get(LOCALHOST)
    
    def tearDown(self):
        self.parent.driver.quit()
        self.parent.app_context.pop()

    def test_signup_functionality(self, username, email, password):
        """Test the signup functionality with parameters."""
        self.parent.driver.get(LOCALHOST)

        self.parent.driver.find_element(By.ID, "login").click()
        self.parent.driver.find_element(By.ID, "create-account").click()

        username_input = self.parent.driver.find_element(By.ID, "signup-username")
        email_input = self.parent.driver.find_element(By.ID, "signup-email")
        password_input = self.parent.driver.find_element(By.ID, "signup-password")
        confirm_password_input = self.parent.driver.find_element(By.ID, "signup-confirm-password")
        signup_submit_button = self.parent.driver.find_element(By.ID, "create-account-button")
        
        username_input.send_keys(username)
        email_input.send_keys(email)
        password_input.send_keys(password)
        confirm_password_input.send_keys(password)
        signup_submit_button.click()
    
    def test_signin_functionality(self, email, password):
        self.parent.driver.get(LOCALHOST)

        self.parent.driver.find_element(By.ID, "login").click()
        self.parent.driver.find_element(By.ID, "login-button").click()
        
        email_input = self.parent.driver.find_element(By.ID, "login-email")
        password_input = self.parent.driver.find_element(By.ID, "login-password")
        login_button = self.parent.driver.find_element(By.ID, "login-button")
        
        email_input.send_keys(email)
        password_input.send_keys(password)
        login_button.click()

        
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
    
    def test_db_activity_addition(self, count):
        testValue = True
        try:
            with self.handler.app_context:
                users = db.session.query(User).all()
                today = datetime.now().date()
                for user in users:
                    for i in range(count):
                        # Randomly scatter activity_date within ±7 days of today
                        day_offset = random.randint(-7, 7)
                        activity_date = today + timedelta(days=day_offset)

                        # Select one of the activity type.
                        activity_type = random.choice(list(ACTIVITY_MET_VALUES.keys()))

                        # Random activity length (10 to 120 minutes)
                        activity_length_minutes = random.randint(10, 120)

                        # Random weight (50kg to 100kg)
                        weight_kg = round(random.uniform(50, 100), 1)

                        # Random distance (500m to 20000m)
                        distance_m = round(random.uniform(500, 20000), 1)

                        # Stagger upload_time by a few seconds for uniqueness
                        t_lib.sleep(0.1 * i)

                        addActivity(
                            upload_user_id=user.id,
                            activity_type=activity_type,
                            activity_date=activity_date,
                            activity_length_minutes=activity_length_minutes,
                            weight_kg=weight_kg,
                            distance_m=distance_m,
                            trail_name=None
                        )
                print(f"Random activity addition test passed: {count} activities per user.")
        except Exception as e:
            testValue = False
            print("Random activity addition test failed")
            print(f"Error Message: {e}")
        return testValue

        
if __name__ == '__main__':
    testing_handler = UnitTestingHandler()
    testing_handler.test_setup()
    database_test_handler = DatabaseTestHandler(testing_handler)
    selenium_test_handler = SeleniumTestHandler(testing_handler)
    database_test_handler.test_database_creation()
    database_test_handler.test_db_user_addition(10)
    database_test_handler.test_password_hashing()
    database_test_handler.test_user_ID()
    database_test_handler.test_db_activity_addition(5)
    #selenium_test_handler.setup_test_server()
    #t_lib.sleep(1)
    #selenium_test_handler.test_signup_functionality("testUser", "testuser@mail.com", "password123")
    #t_lib.sleep(1)
    #selenium_test_handler.test_signin_functionality("testuser@mail.com", "password123")
    # selenium_test_handler.tearDown()
