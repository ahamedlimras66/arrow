from app import app
from db import db
from models.schema import *
from werkzeug.security import check_password_hash, generate_password_hash


db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    if Users.query.filter_by(username="root").first() is None:
        adminID = Users(username="root", password=generate_password_hash("root",method='sha256'),role=1)
        db.session.add(adminID)
        db.session.commit()