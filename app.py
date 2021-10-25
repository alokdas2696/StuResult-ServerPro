from flask import Flask, render_template, session,redirect
from flask_sqlalchemy import SQLAlchemy, request
from flask_mail import *
import json
from random import randint
app = Flask(__name__)
app.secret_key = "login"



with open('config.json','r') as k:
    params = json.load(k)['params']

otp = randint(1111,9999)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/studb'
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = params['gmail-user']
app.config['MAIL_PASSWORD'] = params['gmail-password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

class Student(db.Model):
    stuid = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique= False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    mbno = db.Column(db.String(10), unique=False, nullable=False)
    mtmarks = db.Column(db.Integer(), unique=False, nullable=False)
    scmarks = db.Column(db.Integer(), unique=False, nullable=False)
    csmarks = db.Column(db.Integer(), unique=False, nullable=False)

# @app.route("/display", methods=['GET','POST'])
# def display():
#     if request.method == 'POST':
#         d = request.form.get('rollno')
#         f = Student.query.get(d)
#
#         total = f.mtmarks+f.scmarks+f.csmarks
#
#         per = (total / 300) * 100
#         per = round(per)
#
#
#         # g = f.stuid
#         # i = f.email
#         # j = f.mbno
#
#         return render_template('result.html', data=f, total=total, per=per)
#     return render_template('display.html')

@app.route('/',methods=['GET'])
def home():
      return render_template("email.html")


@app.route('/verify',methods=['GET','POST'])
def verify():
    if request.method == 'POST':
        email = request.form.get('email')
        d = request.form.get('rollno')
        stuid = Student.query.get(d)
        gmail = stuid.email
        if email == gmail:


        # f = Student.query.get(gmail)
        # gmail1 = f.email
        # d = request.form.get('rollno')

            msg = Message('OTP',sender='alokdas9626@gmail.com', recipients=[gmail])
            msg.body = str(otp)
            mail.send(msg)
            return render_template("verify.html",d=d)
        else:
            return " Unmatched EmailID with Roll No"
    return render_template('verify.html')


@app.route('/validate/<int:d>',methods=['GET','POST'])
def validate(d):
    if request.method == 'POST':
        f = Student.query.get(d)
        gmail = f.email
        userotp = request.form['otp']
        if otp == int(userotp):
            # return render_template('send.html',f=f)
            msg = Message('OTP', sender='alokdas9626@gmail.com', recipients=[gmail])
            msg.body = f.name
            mail.send(msg)
            return " Result Send"
        # return render_template('email.html', msg="Not Verified !! try again")
        return render_template('email.html', msg="Not Verified !! try again")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        if username == "admin" and password == "12345":
            session['username'] = username
            # return render_template('send.html', msg=" login successful", username=username)
            return redirect("/admin1")
        else:
            msg = " Invalid username/ password"
            return render_template("login.html", msg=msg)
    return render_template("login.html")








    #         return render_template('send.html',msg="login successful",uname=uname)
    #     else:
    #         msg="Invalid username/ password"
    #         return render_template("/login.html",msg = msg)
    # return render_template("login.html")






# @app.route("/studinfo",methods=['GET','POST'])
# def add():
#     if request.method == 'POST':
#         stuid = request.form.get('stuid')
#         name = request.form.get('name')
#         email = request.form.get('email')
#         mbno = request.form.get('mbno')
#         mtmarks = request.form.get('mtmarks')
#         scmarks = request.form.get('scmarks')
#         csmarks = request.form.get('csmarks')
#
#         entry= Student(stuid=stuid, name=name, email=email, mbno=mbno, mtmarks=mtmarks, scmarks=scmarks, csmarks=csmarks)
#         db.session.add(entry)
#         db.session.commit()
#     return render_template("index1.html")
@app.route("/admin1",methods=['GET'])
def admin1():
    if "username" in session:
        alldata = Student.query.all()
        return render_template("index1.html", alldata=alldata)
    else:
        return redirect("/login")

@app.route("/admin",methods=['POST'])
def add():
    if "username" in session:
        if request.method == 'POST':
            stuid = request.form.get('stuid')
            name = request.form.get('name')
            email = request.form.get('email')
            mbno = request.form.get('mbno')
            mtmarks = request.form.get('mtmarks')
            scmarks = request.form.get('scmarks')
            csmarks = request.form.get('csmarks')

            stu= Student(stuid=stuid, name=name, email=email, mbno=mbno, mtmarks=mtmarks, scmarks=scmarks, csmarks=csmarks)
            db.session.add(stu)
            db.session.commit()

        alldata = Student.query.all()
        return render_template("index1.html",alldata=alldata)
    else:
        return redirect("/login")

# admin Dasboard----------------------
@app.route("/update/<int:stuid>" ,methods=['GET','POST'])
def update(stuid):
    if "username" in session:
        if request.method == 'POST':
            stuid = request.form.get('stuid')
            name = request.form.get('name')
            email = request.form.get('email')
            mbno = request.form.get('mbno')
            mtmarks = request.form.get('mtmarks')
            scmarks = request.form.get('scmarks')
            csmarks = request.form.get('csmarks')
            stu = Student.query.filter_by(stuid=stuid).first()
            # d = Student(stuid=stuid, name=name, email=email, mbno=mbno, mtmarks=mtmarks, scmarks=scmarks,
            #                 csmarks=csmarks)
            # db.session.add(d)
            # db.session.commit()
            stu.stuid = stuid
            stu.name = name
            stu.email = email
            stu.mbno = mbno
            stu.mtmarks = mtmarks
            stu.scmarks = scmarks
            stu.csmarks = csmarks
            db.session.add(stu)
            db.session.commit()
            return redirect("/admin1")
        stu = Student.query.filter_by(stuid=stuid).first()
        return render_template('update.html',stu=stu)
    else:
        return redirect("/login")




@app.route("/delete/<int:stuid>")
def delete(stuid):
    if "username" in session:
        stu = Student.query.filter_by(stuid=stuid).first()
        db.session.delete(stu)
        db.session.commit()
        return redirect("/admin1")
    else:
        return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)