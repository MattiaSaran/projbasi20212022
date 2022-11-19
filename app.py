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
    u = session.query(User).filter_by(email_address = request.form.get('email_address')).first()
    s = session.query(Student).filter_by(id = u.id).first()
    p = session.query(Professor).filter_by(id = u.id).first()
    conn.close()
    if u is not None and request.form.get('password') == u.password:
        if s is not None:
            return redirect(url_for('student', user = u.id))
        elif p is not None:
            return redirect(url_for('professor', user = u.id))
        else:
            return null
    else:
        return redirect(url_for('home'))

@app.route('/student/<user>', methods=['GET'])
def student(user):
    u = session.query(User).filter_by(id = user).first()
    c_id = session.query(Student_Courses).filter_by(STUDENT_ID = user).first()
    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    print(c_id)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    courses = session.query(Course).filter_by(id = c_id.COURSE_ID).first()
    print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
    return render_template('student.html', name = u.first_name + u.last_name, courses = "A") #courses)

@app.route('/professor/<user>', methods=['GET'])
def professor(user):
    u = session.query(User).filter_by(id = user).first()
    courses = session.query(Course.Professor).filter_by(id = user).all()
    return render_template('professor.html', name = u.first_name + u.last_name, courses = courses)

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/adduser', methods = ['POST'])
def adduser():
    if(request.form.get('role') == 'student'):
        user = Student(request.form.get('first_name'), request.form.get('last_name'), request.form.get('email_address'), request.form.get('password'))
        print(user)
        session.add(user)
        session.commit()
        return redirect(url_for('student', user = user))
    elif(request.form.get('role') == 'professor'):
        user = Professor(request.form.get('first_name'), request.form.get('last_name'), request.form.get('email_address'), request.form.get('password'))
        session.add(user)
        session.commit()
        return redirect(url_for('professor', user = user))
    else:
        return redirect(url_for('home'))

@app.route('/student_course')
def student_course(user, course):
    return render_template('student_course.html', user = user, course = course)

@app.route('/professor_course')
def professor_course(user, course):
    return render_template('professor_course.html', user = user)

@app.route('/create_course', methods = ['POST'])
def create_course(user):
    course = Course(request.form.get('name'), request.form.get('capacity'))
    session.add(course)
    session.commit()
    return redirect(url_for('professor_course', user = user, course = course))

@app.route('/add_course', methods = ['GET','POST'])
def add_course(user):
    course = session.query(Course).filter_by(name = request.form.get('name')).first()
    user.Courses.append(course)
    return redirect(url_for('student_course', user = user, course = course))

@app.route('/new_lecture')
def new_lecture(course):
    return render_template('new_lecture.html', course = course)

@app.route('/add_lecture', methods = ['POST'])
def add_lecture(user, course):
    lecture = Lectures(request.form.get('date'), request.form.get('mode'), request.form.get('classroom'))
    session.add(lecture)
    session.commit()
    return redirect(url_for('professor_course', user = user, course = course))

@app.route('/update/<lecture>')
def update_lecture(lecture):
    return render_template('update_lecture.html', lecture = lecture)

@app.route('/update/<course>')
def update_course(course):
    return render_template('update_course.html', course = course)

@app.route('/modify/<lecture>', methods = ['GET', 'POST'])
def modify_lecture(lecture):
    session.query(Lectures).filter_by(id = lecture.id).first()
    update({Lectures.date:request.form.get('date'), Lectures.mode:request.form.get('mode'), Lectures.classroom:request.form.get('classroom')}, synchronize_session = False)
    session.commit()

@app.route('/modify/<course>', methods = ['GET', 'POST'])
def modify_course(course):
    session.query(Course).filter_by(id = course.id).first()
    update({Course.name:request.form.get('name'), Course.capacity:request.form.get('capacity')}, synchronize_session = False)
    session.commit()

@app.route('/other_courses')
def other_courses(user):
    return render_template('other_courses.html', user = user)
