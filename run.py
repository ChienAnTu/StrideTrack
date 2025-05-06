from app import create_app, db
from app.models import User

app = create_app()

def testAddition(user_id, name, email):
    to_add = User(username=name, user_id = user_id, email = email)
    db.session.add(to_add)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    