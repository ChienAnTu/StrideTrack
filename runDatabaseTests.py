from app import create_app, db
import Tests
from app.config import Config, TestingConfig
from app.models import User, ActivityRegistry, SharedActivity

app = create_app(Config)
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.query(User).delete() # Clears all of the database for testing. Since there is no commit this will not reflect the real DB.
        Tests.addRandomUsers(20)
        for user in (db.session.query(User).all()):
            print(user.email)