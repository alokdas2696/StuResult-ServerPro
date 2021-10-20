from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy, request
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/studb'
db= SQLAlchemy(app)

class Student(db.Model):
    stuid = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique= False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    mbno = db.Column(db.String(10), unique=False, nullable=False)
    mtmarks = db.Column(db.Integer(), unique=False, nullable=False)
    scmarks = db.Column(db.Integer(), unique=False, nullable=False)
    csmarks = db.Column(db.Integer(), unique=False, nullable=False)

@app.route("/", methods=['GET','POST'])
def display():
    if request.method == 'POST':
        d = request.form.get('rollno')
        f = Student.query.get(d)

        total = f.mtmarks+f.scmarks+f.csmarks
        print(total)
        per = (total / 300) * 100
        per = round(per)
        print(per)

        # g = f.stuid
        # i = f.email
        # j = f.mbno

        return render_template('result.html', data=f, total=total, per=per)
    return render_template('display.html')


@app.route("/studinfo",methods=['GET','POST'])
def info():
    if request.method == 'POST':
        stuid = request.form.get('stuid')
        name = request.form.get('name')
        email = request.form.get('email')
        mbno = request.form.get('mbno')
        mtmarks = request.form.get('mtmarks')
        scmarks = request.form.get('scmarks')
        csmarks = request.form.get('csmarks')

        entry= Student(stuid=stuid, name=name, email=email, mbno=mbno, mtmarks=mtmarks, scmarks=scmarks, csmarks=csmarks)
        db.session.add(entry)
        db.session.commit()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)