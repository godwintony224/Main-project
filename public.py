from flask import *
from database import *
import uuid

import ctypes
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

public=Blueprint('public',__name__)


@public.route('/',methods=['get','post'])
def index():
	return render_template('index.html')

@public.route('/login',methods=['get','post'])
def login():
	if 'submit' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="select*from login where username='%s' and password='%s'"%(username,password)
		res=select(q)
		if len(res) > 0:
			session['login_id']=res[0]['login_id']
			if res[0]['usertype']=="admin":
				flash("Login Successfully")
				return redirect(url_for('admin.adminhome'))
			if res[0]['usertype']=="user":

				# ids=res[0]['login_id']
				# r = "select * from user where login_id='%s'" % (ids)
				# re = select(r)
				# resetemail=re[0]['email']
				# email_sender = 'pixo.streaming@gmail.com'
				# email_receiver = resetemail
				# subject = 'OTP for Login'
				# msg = MIMEMultipart()
				# msg['From'] = email_sender
				# msg['To'] = email_receiver
				# msg['Subject'] = subject
				#
				# global n
				# n = random.randint(111111, 999999)
				#
				# body = 'Greetings from pixo, \n %d is the OTP to reset your password.' % (n)
				#
				# msg.attach(MIMEText(body, 'plain'))
				# text = msg.as_string()
				#
				# connection = smtplib.SMTP('smtp.gmail.com', 587)
				# connection.starttls()
				# connection.login(email_sender, 'Pixo@2022')
				# connection.sendmail(email_sender, email_receiver, text)
				# connection.quit()

				flash("Login Successfully")
				return redirect(url_for('user.userhome'))
			if res[0]['usertype']=="Candidate":
				flash("Login Successfully")
				return redirect(url_for('candidate.canhome'))
			if res[0]['usertype'] == "teacher":
				flash("Login Successfully")
				return redirect(url_for('teacher.teacherhome'))
		else:
			flash("Invalid username or password")
	return render_template('login.html')

@public.route('/user_register',methods=['get','post'])
def user_register():
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		photo=request.files['image']
		path='static/uploads/'+str(uuid.uuid4())+photo.filename
		photo.save(path)
		gender=request.form['gender']
		department = request.form['department']
		address=request.form['address']
		phone=request.form['phone']
		email=request.form['email']
		number=request.form['number']
		username=request.form['username']
		password=request.form['password']
		q="select * from login   where  username='%s' and password='%s' "%(username,password)
		res=select(q)
		if len(res)>0:
			flash("Fake Voter-ID")
		elif len(res)>0:
			flash("Fake Username and Password")
		else:
			q="insert into login values(null,'%s','%s','user')"%(username,password)
			res=insert(q)
			q="insert into user values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(res,fname,lname,path,gender,department,address,phone,email,number)
			result=insert(q)
			flash("Registered Successfully")
			application = 'requesting access'
			q = "insert into userapplication values(null,'%s','pending','%s',Curdate())" % (
				result, application)
			insert(q)
			flash("Application Sended")
	return render_template('user_register.html')


@public.route('/teacher_register', methods=['get', 'post'])
def teacher_register():
	if 'submit' in request.form:
		fname = request.form['fname']
		lname = request.form['lname']
		photo = request.files['image']
		path = 'static/uploads/' + str(uuid.uuid4()) + photo.filename
		photo.save(path)
		gender = request.form['gender']
		department = request.form['department']
		address = request.form['address']
		phone = request.form['phone']
		email = request.form['email']
		number = request.form['number']
		photos = request.files['images']
		path1 = 'static/uploads1/' + str(uuid.uuid4()) + photos.filename
		photos.save(path1)
		username = request.form['username']
		password = request.form['password']
		q = "select * from login where username='%s' and password='%s'" % (username, password)
		res = select(q)
		if len(res) > 0:
			flash("Already Exists")
		else:
			q = "insert into login values(null,'%s','%s','teacher')" % (username, password)
			res = insert(q)
			q = "insert into teacher values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
			res, fname, lname, path, gender, department, address, phone, email, number, path1)
			result=insert(q)
			flash("Registered Successfully")
			application = 'requesting access'
			q = "insert into teacherapplication values(null,'%s','pending','%s',Curdate())" % (
				result, application)
			insert(q)
			flash("Application Sended")
	return render_template('teacher_register.html')\

@public.route('/view_result',methods=['get','post'])
def view_result():
	data={}
	q="SELECT COUNT(`status`), candidate_id,concat(fname,' ',lname)as NAME FROM voting INNER JOIN candidates USING(candidate_id) GROUP BY candidate_id"
	res=select(q)
	data['re']=res
	return render_template('view_result.html',data=data)