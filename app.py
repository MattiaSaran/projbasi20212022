from db import *
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return session.query(User).filter_by(id = id).first()

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
            login_user(u)
            return redirect(url_for('student'))
        elif p is not None:
            login_user(u)
            return redirect(url_for('professor'))
        else:
            return null
    else:
        return redirect(url_for('home'))

@app.route('/student', methods=['GET'])
@login_required
def student():
    c_id = session.query(Student_Courses).filter_by(STUDENT_ID = current_user.id).all()
    if c_id is not None:
        courses = list()
        for i in c_id:
            courses.append(session.query(Course).filter_by(id = i.c.COURSE_ID).first())
    else:
        courses = None
    return render_template('student.html', user = current_user, courses = courses)

@app.route('/professor/<user>', methods=['GET'])
@login_required
def professor():
    courses = session.query(Course).filter_by(professor_id = current_user.id).all()
    return render_template('professor.html', user = current_user, courses = courses)

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
        return redirect(url_for('home'))
    elif(request.form.get('role') == 'professor'):
        user = Professor(request.form.get('first_name'), request.form.get('last_name'), request.form.get('email_address'), request.form.get('password'))
        session.add(user)
        session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/student_course')
@login_required
def student_course(course):
    return render_template('student_course.html', user = current_user, course = course)

@app.route('/professor_course')
@login_required
def professor_course(course):
    return render_template('professor_course.html', user = current_user, course = course)

@app.route('/create_course', methods = ['POST'])
@login_required
def create_course():
    course = Course(request.form.get('name'), request.form.get('capacity'))
    session.add(course)
    session.commit()
    return redirect(url_for('professor_course', user = current_user, course = course))

@app.route('/add_course', methods = ['GET','POST'])
@login_required
def add_course():
    course = session.query(Course).filter_by(name = request.form.get('name')).first()
    current_user.Courses.append(course)
    return redirect(url_for('student_course', user = current_user, course = course))

@app.route('/new_lecture')
@login_required
def new_lecture(course):
    return render_template('new_lecture.html', course = course)

@app.route('/add_lecture', methods = ['POST'])
@login_required
def add_lecture(course):
    lecture = Lectures(request.form.get('date'), request.form.get('mode'), request.form.get('classroom'))
    session.add(lecture)
    session.commit()
    return redirect(url_for('professor_course', user = current_user, course = course))

@app.route('/update/<lecture>')
@login_required
def update_lecture(lecture):
    return render_template('update_lecture.html', lecture = lecture)

@app.route('/update/<course>')
@login_required
def update_course(course):
    return render_template('update_course.html', course = course)

@app.route('/modify/<lecture>', methods = ['GET', 'POST'])
@login_required
def modify_lecture(lecture):
    session.query(Lectures).filter_by(id = lecture.id).first()
    update({Lectures.date:request.form.get('date'), Lectures.mode:request.form.get('mode'), Lectures.classroom:request.form.get('classroom')}, synchronize_session = False)
    session.commit()

@app.route('/modify/<course>', methods = ['GET', 'POST'])
@login_required
def modify_course(course):
    session.query(Course).filter_by(id = course.id).first()
    update({Course.name:request.form.get('name'), Course.capacity:request.form.get('capacity')}, synchronize_session = False)
    session.commit()

@app.route('/other_courses')
@login_required
def other_courses(user):
    return render_template('other_courses.html', user = user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))