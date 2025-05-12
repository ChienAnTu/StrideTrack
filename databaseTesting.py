from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import random
from random_username.generate import generate_username

def addUser(name, email):
    to_add = User(username=name, email = email, password_hash = generate_password_hash(str(random.randint(1000,9999))))
    db.session.add(to_add)

class TestingClass:
    def generateUsers(self,count):
        self.count = count
        self.random_users = generate_username(count)
        
    def addRandomUsers(self):
        for user in self.random_users:
            username = user
            email = user + "@mail.com"
            addUser(username, email)
    
    def testLength(self, db):
        if db.session.query(User).all() == self.count: 
            print("Count test passed")
        else:
            print("Count test failed")