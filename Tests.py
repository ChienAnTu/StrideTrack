from app import create_testing_app, db
from app.models import User, ActivityRegistry, SharedActivity
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

# Simple test to add a user to the database.
def addUser(name, email, password_hash):
    to_add = User(username=name, email = email, password_hash = password_hash)
    db.session.add(to_add)
    db.session.commit()

# Add an activity to the database for testing database.
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

# Add an activity that is shared between two users to test the db
def addSharedActivity(activity_id: int, user_shared_with: str, sharing_user_id: int):
    shared = SharedActivity(
        activity_id=activity_id,
        user_shared_with=user_shared_with,
        sharing_user_id=sharing_user_id
    )
    db.session.add(shared)
    db.session.commit()

# Initialize the test server
def create_test_server():
    """Creates and runs the Flask test server."""
    app = create_testing_app(TestingConfig)
    app.run()

# Class that handles and stores data across the unit tests
class UnitTestingHandler(unittest.TestCase):
    # Sets up flask app.
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
    # Handles the Selenium Tests
    def __init__(self, parent):
        self.parent = parent
    
    def setup_test_server(self):
        # Setups the test server and start the Chrome Driver
        self.parent.server_thread = multiprocessing.Process(target=create_test_server)
        self.parent.driver = webdriver.Chrome()
        self.parent.server_thread.start()
        self.parent.driver.get(LOCALHOST)
    
    def tearDown(self):
        # Small teardown to exit the app
        self.parent.driver.quit()
        self.parent.app_context.pop()

    def test_signup_functionality(self, username, email, password):
        # Test signup function in the app, tries to sign up with the provided params
        self.parent.driver.get(LOCALHOST)
        try:
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
            t_lib.sleep(1)
            # Query the database for the user
            user = None
            try:
                with self.parent.app_context:
                    user = db.session.query(User).filter_by(email=email).first()
            except Exception as db_e:
                print(f"Database query error during signup test: {db_e}")
            if user is not None:
                return True
            else:
                return False
        except Exception as e:
            print(f"Signup test encountered an error for user: {username}. Error: {e}")
            return False

    def test_signin_functionality(self, email, password):
        # Test the sign in feature with the provided params
        self.parent.driver.get(LOCALHOST)
        try:
            self.parent.driver.find_element(By.ID, "login").click()
            email_input = self.parent.driver.find_element(By.ID, "login-email")
            password_input = self.parent.driver.find_element(By.ID, "login-password")
            login_button = self.parent.driver.find_element(By.ID, "login-button")
            email_input.send_keys(email)
            password_input.send_keys(password)
            login_button.click()
            t_lib.sleep(1)
            # Try to find the login button again; if not found, login succeeded
            try:
                self.parent.driver.find_element(By.ID, "login")
                return False
            except Exception:
                return True
        except Exception as e:
            print(f"Signin test encountered an error for email: {email}. Error: {e}")
            return False

    def test_logout_functionality(self):
        # CLick on the logout button and see if it works
        self.parent.driver.get(LOCALHOST)
        try:
            self.parent.driver.find_element(By.ID, "logout").click()
            t_lib.sleep(1)
            # Try to find the logout button again; if not found, logout succeeded
            try:
                self.parent.driver.find_element(By.ID, "logout")
                return False
            except Exception:
                return True
        except Exception as e:
            print(f"Logout test encountered an error. Error: {e}")
            return False

    def test_site_navigation(self):
        # Navigates through all of the pages on the site to check
        sidebar_routes = [
            ("/dashboard", "Dashboard"),
            ("/share", "My Activities"),
            ("/shared_with_me", "Shared With Me"),
            ("/challenges", "Challenges"),
            ("/visualise", "Progress"),
            ("/calories", "Upload Data")
        ]
        all_passed = True
        for route, expected_text in sidebar_routes:
            try:
                url = LOCALHOST.rstrip('/') + route
                self.parent.driver.get(url)
                t_lib.sleep(1)
                page_source = self.parent.driver.page_source
                if expected_text not in page_source:
                    all_passed = False
            except Exception as e:
                print(f"Site navigation test encountered an error for '{route}': {e}")
                all_passed = False
        return all_passed

    def test_dashboard_header_link(self):
        # Goes to the dashboard from the header link!
        self.parent.driver.get(LOCALHOST)
        t_lib.sleep(1)
        try:
            dashboard_link = self.parent.driver.find_element(By.ID, "header-dashboard")
            dashboard_link.click()
            t_lib.sleep(1)
            current_url = self.parent.driver.current_url
            if "/dashboard" in current_url:
                return True
            else:
                return False
        except Exception as e:
            print(f"Header dashboard link navigation test encountered an error: {e}")
            return False
        
    def test_calories_manual_upload(self):
        # Manually uploads a new file
        import random
        self.parent.driver.get(LOCALHOST.rstrip('/') + '/calories')
        t_lib.sleep(1)
        try:
            # Select a random activity
            activity_options = ["walking", "running", "cycling", "hiking", "swimming", "yoga"]
            activity = random.choice(activity_options)
            duration = random.randint(10, 120)
            weight = random.randint(50, 100)
            distance = random.randint(100, 600)

            activity_select = self.parent.driver.find_element(By.ID, "activity")
            for option in activity_select.find_elements(By.TAG_NAME, 'option'):
                if option.get_attribute('value') == activity:
                    option.click()
                    break
            self.parent.driver.find_element(By.ID, "duration").clear()
            self.parent.driver.find_element(By.ID, "duration").send_keys(str(duration))
            self.parent.driver.find_element(By.ID, "weight").clear()
            self.parent.driver.find_element(By.ID, "weight").send_keys(str(weight))
            self.parent.driver.find_element(By.ID, "distance_m").clear()
            self.parent.driver.find_element(By.ID, "distance_m").send_keys(str(distance))

            self.parent.driver.find_element(By.ID, "submit-manual").click()
            t_lib.sleep(2)

            # Query the database for the activity to check if it is successful
            activity_found = False
            try:
                with self.parent.app_context:
                    user = db.session.query(User).filter_by(email=self.parent.logged_in_user).first()
                    if user:
                        # Find the most recent activity for this user
                        recent_activity = db.session.query(ActivityRegistry).filter_by(
                            upload_user_id=user.id,
                            activity_type=activity,
                            weight_kg=weight,
                            distance_m=distance
                        ).order_by(ActivityRegistry.upload_time.desc()).first()
                        if recent_activity and abs((recent_activity.activity_length.hour * 60 + recent_activity.activity_length.minute) - duration) <= 2:
                            activity_found = True
            except Exception as db_e:
                print(f"Database query error during calories upload test: {db_e}")
            return activity_found
        except Exception as e:
            print(f"Calories manual upload test encountered an error: {e}")
            return False

class DatabaseTestHandler():
    # Class that handles all of the database testing
    def __init__(self, parent):
        self.handler = parent
        
    def test_database_creation(self):
        # Creates the database tables
        try:
            with self.handler.app_context:
                db.create_all()
            return True
        except Exception as e:
            return False

    def test_db_user_addition(self, count):
        # Test adding a new user to the database
        try:
            self.handler.test_users = generate_username(count)
            self.handler.user_password_dictionary = {}
            self.handler.user_passwordHash_dictionary = {}
            with self.handler.app_context:
                for user in self.handler.test_users:
                    password = list(user)
                    random.shuffle(password)
                    password = "".join(password)
                    password_hash = generate_password_hash(password)
                    addUser(user, user + "@mail.com", password_hash=password_hash)
                    self.handler.user_password_dictionary[user] = password
                    self.handler.user_passwordHash_dictionary[user] = password_hash
                added_users = db.session.query(User).all()
                if len(added_users) == len(self.handler.test_users):
                    self.handler.users_in_db = added_users
                    return True
                else:
                    return False
        except Exception as e:
            return False

    def test_password_hashing(self):
        # Test the hashing feature in the database, checks whether the password is recognized or not
        try:
            with self.handler.app_context:
                for user in self.handler.test_users:
                    if not check_password_hash(self.handler.user_passwordHash_dictionary[user], self.handler.user_password_dictionary[user]):
                        return False
            return True
        except Exception as e:
            return False

    def test_user_ID(self):
        # Check if the user ID increment is working or not
        try:
            counter = 1
            for user in self.handler.users_in_db:
                if user.id != counter:
                    return False
                counter += 1
            return True
        except Exception as e:
            return False

    def test_db_activity_addition(self, count):
        # Generate an activity for the user
        try:
            with self.handler.app_context:
                users = db.session.query(User).all()
                today = datetime.now().date()
                for user in users:
                    for i in range(count):
                        day_offset = random.randint(-7, 7) # Days can be from 7 days before or after.
                        activity_date = today + timedelta(days=day_offset)
                        activity_type = random.choice(list(ACTIVITY_MET_VALUES.keys()))
                        activity_length_minutes = random.randint(10, 120)
                        weight_kg = round(random.uniform(50, 100), 1)
                        distance_m = round(random.uniform(500, 20000), 1)
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
            return True
        except Exception as e:
            return False

    def test_db_shared_activity_addition(self, count):
        # Adds a shared activity between users
        try:
            with self.handler.app_context:
                users = db.session.query(User).all()
                user_emails = {user.id: user.email for user in users}
                for user in users:
                    possible_others = [u for u in users if u.id != user.id]
                    if not possible_others:
                        continue
                    for _ in range(count):
                        other_user = random.choice(possible_others)
                        activities = db.session.query(ActivityRegistry).filter_by(upload_user_id=other_user.id).all()
                        if not activities:
                            continue
                        activity = random.choice(activities)
                        addSharedActivity(
                            activity_id=activity.id,
                            user_shared_with=user_emails[user.id],
                            sharing_user_id=other_user.id
                        )
            return True
        except Exception as e:
            return False


def run_back_end_test(testing_handler):
    start_time = t_lib.time() # Used for calculating how long each test took
    database_test_handler = DatabaseTestHandler(testing_handler)
    results = {}
    results['test_database_creation'] = database_test_handler.test_database_creation()
    results['test_db_user_addition'] = database_test_handler.test_db_user_addition(10)
    results['test_password_hashing'] = database_test_handler.test_password_hashing()
    results['test_user_ID'] = database_test_handler.test_user_ID()
    results['test_db_activity_addition'] = database_test_handler.test_db_activity_addition(3)
    results['test_db_shared_activity_addition'] = database_test_handler.test_db_shared_activity_addition(1)
    end_time = t_lib.time()  # End timer
    elapsed = end_time - start_time
    print("\nBack End Testing Finished: Total test time: {:.2f} seconds".format(elapsed))
    return results

def run_selenium_test(testing_handler):
    selenium_test_handler = SeleniumTestHandler(testing_handler)
    selenium_test_handler.setup_test_server()
    results = {}
    results['test_signup_functionality'] = selenium_test_handler.test_signup_functionality("testUser", "testuser@mail.com", "pqsaeyg1!@#uir")
    # The Results is flipped for this as False = it passed
    if (selenium_test_handler.test_signin_functionality("testuser@mail.com", "pqweeqweqw")): 
        results['test_signin_wrong_password'] = False
    else:
        True
    results['test_signup_same_email'] = selenium_test_handler.test_signup_functionality("testUser", "testuser@mail.com", "pqsaeyg1!@#uir")
    results['test_signin_correct_password'] = selenium_test_handler.test_signin_functionality("testuser@mail.com", "pqsaeyg1!@#uir")
    results['test_logout_functionality'] = selenium_test_handler.test_logout_functionality()
    results['test_signin_random_user'] = selenium_test_handler.test_signin_functionality(
        testing_handler.test_users[0] + "@mail.com", testing_handler.user_password_dictionary[testing_handler.test_users[0]]
    )
    testing_handler.logged_in_user = testing_handler.test_users[0] + "@mail.com" # For verifying the calories manual upload later
    results['test_dashboard_header_link'] = selenium_test_handler.test_dashboard_header_link()
    results['test_site_navigation'] = selenium_test_handler.test_site_navigation()
    results['test_calories_manual_upload'] = selenium_test_handler.test_calories_manual_upload()
    selenium_test_handler.tearDown()
    print("Selenium Testing Finished")
    return results

def parseResults(backend_results, selenium_results):
    print("Back End Test Results:")
    for test, passed in backend_results.items():
        print(f"  {test}: {'PASSED' if passed else 'FAILED'}")
    print("Selenium Test Results:")
    for test, passed in selenium_results.items():
        print(f"  {test}: {'PASSED' if passed else 'FAILED'}")
    
    
if __name__ == '__main__':
    testing_handler = UnitTestingHandler()
    testing_handler.test_setup()
    back_end_result = run_back_end_test(testing_handler)
    selenium_result = run_selenium_test(testing_handler)
    
    parseResults(back_end_result, selenium_result)