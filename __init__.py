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
    s = Student.query.all()
    conn.close()
    a = []
    #usare righe sotto commentate se il secondo if non funziona
    #for row in s:
    #    a.append(row)
    if u is not None and request.form['password'] == u.password:
        if u in s:
            redirect(url_for('student', user=u))
        else:
            redirect(url_for('professor', user=u))
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
    course = Course(request.form['name'], request.form['capacity'])
    session.add(course)
    session.commit()
    return redirect(url_for('professor_course', user=user, course=course))

@app.route('/add_course', methods=['POST'])
def add_course(user):
    course = Course.query.filter_by(name=request.form['name']).first()
    user.Courses.append(course)
    return redirect(url_for('student_course', user=user, course=course))

@app.route('/new_lecture')
def new_lecture(course):
    return render_template('new_lecture.html', course=course)

@app.route('/add_lecture', methods=['POST'])
def add_lecture(user, course):
    lecture = Lectures(request.form['date'], request.form['mode'], request.form['classroom'])
    session.add(lecture)
    session.commit()
    return redirect(url_for('professor_course', user=user, course=course))

@app.route('/update_lecture')
def update_lecture(lecture):
    return render_template('update_lecture.html', lecture = lecture)

@app.route('/update_course')
def update_course(course):
    return render_template('update_course.html', course = course)

@app.route('/modify_lecture', methods=['GET', 'POST'])
def modify_lecture(lecture):
    session.query(Lectures).filter_by(id=lecture.id).first()
    update({Lectures.date:request.form['date'], Lectures.mode:request.form['mode'], Lectures.classroom:request.form['classroom']}, synchronize_session = False)
    session.commit()

@app.route('/modify_course', methods=['GET', 'POST'])
def modify_course(course):
    session.query(Course).filter_by(id=course.id).first()
    update({Course.name:request.form['name'], Course.capacity:request.form['capacity']}, synchronize_session = False)
    session.commit()

@app.route('/other_courses')
def other_courses(user):
    return render_template('other_courses.html', user=user)
