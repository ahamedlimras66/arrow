import os
from models.schema import *
from flask_admin import Admin, AdminIndexView
from flask import Flask, render_template, send_file, request, url_for, redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'my-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_first_request
def create_tables():
	db.create_all()
	if User.query.filter_by(username="root").first() is None:
		adminID = User(username="root", password="root")
		db.session.add(adminID)
	db.session.commit()

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and (current_user.username == 'root'):
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and (current_user.username == 'root'):
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class UserRoleView(MyModelView):
    column_list = ('role', 'user.username')

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(ModelView(User, db.session))
admin.add_view(UserRoleView(UserRole, db.session))


# Home page
@app.route('/')
def home():
	return render_template("index.html")

# login page
@app.route('/login')
def login():
	return render_template('login.html')

# check login "username" and "password"
@app.route('/login_check', methods=['POST', 'GET'])
def loginCheck():
	userName = request.form['username']
	password = request.form['password']
	print(userName, password)
	user = User.query.filter_by(username=userName).first()
	if user:
		if user.password == password:
			login_user(user, remember=False)
			return render_template("course.html")
	else:
		return render_template('login.html')

# course materials
@app.route('/course')
@login_required
def course():
	return render_template("course.html")
@app.route('/online')
def onlinet():
    return render_template("online.html")

@app.route('/contact')
def contact():
    return render_template("contact.html") 
@app.route('/achieve')
def achievement():
    return render_template("achieve.html")
@app.route('/gallery')
def gallery():
    return render_template("gal.html")
   

# To Download course material by code
@app.route('/return-files', methods=['POST'])
def return_files_tut():
	fileName = request.form['subjectcode'] + ".pdf"
	try:
		return send_file('notes/'+fileName, attachment_filename=fileName)
	except Exception as e:
		return str(e)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return render_template('index.html')
if __name__ == "__main__":
	from db import db
	db.init_app(app)
	app.run(debug=True)
