from db import *
from flask import Flask
from flask import render_template,request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = engine.connect()
    u = User.query.filter_by(request.form['email'])
    #da sistemare riga sotto
    s = Student.query.all()
    conn.close()
    if u is not None and request.form['password'] == u.password:
        #da sistemare righe commentate sotto
        #if u is in s:
            #redirect(url_for('student', user=u))
        #else:
            #redirect(url_for('professor', user=u))
        return null #placeholder
    else:
        return redirect(url_for('home'))

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/student', methods=['GET'])
def student(user):
    courses = Course.query.filter_by(student=user).first()
    return render_template('student.html', user=user, courses=courses)

@app.route('/professor', methods=['GET'])
def professor(user):
    courses = Course.query.filter_by(professor=user).first()
    return render_template('professor.html', user=user, courses=courses)

@app.route('/add_user', methods=['POST'])
def add_user():
    if(request.form['role']=='student'):
        user = Student(request.form['first_name'], request.form['last_name'], request.form['email_address'], request.form['password'])
        session.add(user)
        session.commit()
        return redirect(url_for('student', user=user))
    elif(request.form['role']=='professor'):
        user = Professor(request.form['first_name'], request.form['last_name'], request.form['email_address'], request.form['password'])
        session.add(user)
        session.commit()
        return redirect(url_for('professor', user=user))
    else:
        return redirect(url_for('home'))

@app.route('/student_course')
def student_course(user, course):
    return render_template('student_course.html', user=user, course=course)

@app.route('/professor_course')
def professor_course(user, course):
    return render_template('professor_course.html', user=user)

@app.route('/create_course', methods=['POST'])
def create_course(user):
    #id placeholder
    course = Course( "a", request.form['name'], request.form['capacity'])
    session.add(course)
    session.commit()
    return redirect(url_for('professor_course', user=user, course=course))

#add a course to a student curriculum
@app.route('/add_course', methods=['POST'])
def add_course(user):
    #da completare
    course = 1 #placeholder
    return redirect(url_for('student_course', user=user, course=course))

@app.route('/new_lecture')
def new_lecture(course):
    return render_template('new_lecture.html', course=course)

@app.route('/add_lecture', methods=['POST'])
def add_lecture(user, course):
    #id placeholder
    lecture = Lectures( "a" , request.form['date'], request.form['mode'], request.form['classroom'])
    session.add(lecture)
    session.commit()
    return redirect(url_for('professor_course', user=user, course=course))

@app.route('/update_lecture')
def update_lecture(lecture):
    return render_template('update_lecture.html')

@app.route('/update_course')
def update_course(course):
    return render_template('update_course.html')

@app.route('/modify_lecture')
def modify_lecture(lecture):
    #placeholder, da cambiare
    lecture.modify()

@app.route('/modify_course')
def modify_course(course):
    #placeholder, da cambiare
    course.modify()

@app.route('/other_courses')
def other_courses(user):
    return render_template('other_courses.html', user=user)
