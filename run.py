from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    if Users.query.filter_by(username="root").first() is None:
        adminID = Users(username="root", password="root",role=1)
        db.session.add(adminID)
        db.session.commit()