from db import *
from flask import Flask
from flask import render_template,request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/student/<name>')
def student(email):
    user = Student.query.filter_by(email=email).first()
    return render_template('student.html', user=user)

@app.route('/professor/<name>')
def professor(email):
    user = Professor.query.filter_by(email=email).first()
    return render_template('professor.html', user=user)

@app.route('/add_user', methods=['POST'])
def add_user():
    if(request.form['role']=='student'):
        user = Student(request.form['first_name'], request.form['last_name'], request.form['email_address'], request.form['password'])
        session.add(user)
        session.commit()
        return redirect(url_for('student', email=user.email_address))
    elif(request.form['role']=='professor'):
        user = Professor(request.form['first_name'], request.form['last_name'], request.form['email_address'], request.form['password'])
        session.add(user)
        session.commit()
        return redirect(url_for('professor', email=user.email_address))
    else:
        return redirect(url_for('home'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('student/course/<name>')
def student_course(name):
    return render_template('student_course.html', name=name)

@app.route('/professor/course/<name>')
def professor_course(name):
    return render_template('professor_course.html', name=name)

@app.route('/professor/course/<name>/lecture')
def new_lecture(name):
    return render_template('new_lecture.html', name=name)

@app.route('/student/<name>/othercourses')
def other_courses(name):
    return render_template('other_courses.html', name=name)
