import os
from models.schema import *
from flask_mail import Mail,Message
from werkzeug.security import check_password_hash, generate_password_hash
from flask_admin import Admin, AdminIndexView
from flask import Flask, render_template, send_file, request, url_for, redirect, send_from_directory
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__,static_folder='static')
app.secret_key = 'my-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'arrowcoaching26@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mithran12'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_first_request
def create_tables():
	db.create_all()
	if Users.query.filter_by(username="root").first() is None:
		adminID = Users(username="root", password=generate_password_hash("root",method='sha256'),role=1)
		db.session.add(adminID)
		db.session.commit()

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		if current_user.is_authenticated  and (current_user.role<3):
			return True
	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login', next=request.url))

class MyModelView(ModelView):
	def is_accessible(self):
		if current_user.is_authenticated  and (current_user.role<3):
			return True
	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login', next=request.url))

class UserAdmin(ModelView):
    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password,method='sha256')


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(UserAdmin(Users, db.session))
admin.add_view(MyModelView(ExamLink, db.session))
admin.add_view(MyModelView(Number, db.session))


@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

# Home page
@app.route('/')
def home():
	return render_template("index.html")


@app.route('/save_number', methods=['POST', 'GET'])
def save_number():
	number = request.form['number']
	print(Number.query.filter_by(number=number).first())
	if Number.query.filter_by(number=number).first():
		error = "Phone number already exist"
		return render_template('index.html',error=error)
	else:
		number = Number(number=request.form['number'],name="unknow")
		db.session.add(number)
		db.session.commit()
		return redirect("tel:+919677529252")


# login page
@app.route('/login')
def login():
	return render_template('login.html')


# check login "username" and "password"
@app.route('/login_check', methods=['POST', 'GET'])
def loginCheck():
	userName = request.form['username']
	password = request.form['password']
	user = Users.query.filter_by(username=userName).first()
	if user and check_password_hash(user.password, password):
		login_user(user, remember=False)
		if user.role <=2:
			return redirect('admin')
		return render_template("course.html")
	error = "Incorrect username or password"
	return render_template('login.html',error=error)


# course materials
@app.route('/course')
@login_required
def course():
	return render_template("course.html")


@app.route('/online')
def onlinet():
	exam = ExamLink.query.first()
	if exam is None:
		return render_template("online.html")
	return render_template("online.html",link=exam.link)


@app.route('/contact')
def contact():
    return render_template("contact.html") 


@app.route('/achieve')
def achievement():
    return render_template("achieve.html")


@app.route('/gallery')
def gallery():
    return render_template("gal.html")


@app.route('/admission')
def admission():
    return render_template("admission.html")


@app.route('/apply_admission', methods=['POST'])
def apply_admission():
	new_admission = Admission(name=request.form['name'],
							  email=request.form['email'],
							  phone_no=request.form['number'],
							  dob=request.form['dob'],
							  group=request.form['group'])
	db.session.add(new_admission)
	db.session.commit()
	msg = Message("hello", sender="arrowmail", recipients=['satheesh2910@gmail.com'])
	msg.html = render_template("admissionmail.html",
								name=new_admission.name,
								mail=new_admission.email,
								number=new_admission.phone_no,
								DOB=new_admission.dob,
								Group=new_admission.group)
	mail.send(msg)
	return render_template("index.html")
   

# To Download course material by code
@app.route('/return-files', methods=['POST'])
def return_files_tut():
	fileName = request.form['subjectcode'].lower() + ".pdf"
	try:
		return send_file('notes/'+fileName, attachment_filename=fileName)
	except Exception as e:
		error = "subject code is not found pleass check below"
		return render_template("course.html",error=error)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return render_template('index.html')


if __name__ == "__main__":
	from db import db
	db.init_app(app)
	app.run(debug=True)
