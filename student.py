from db import *
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask import Blueprint

student = Blueprint('student', __name__, url_prefix='/student')

@student.route('/', methods=['GET'])
@login_required
def page():
    c_id = session.query(Student_Course).filter_by(student_id = current_user.id).all()
    if c_id is not None:
        courses = list()
        for i in c_id:
            courses.append(session.query(Course).filter_by(id = i.course_id).first())
    else:
        courses = None
    return render_template('student.html', user = current_user, courses = courses)

@student.route('/<courseid>')
@login_required
def course(courseid):
    course = session.query(Course).filter_by(id = courseid).first()
    return render_template('student_course.html', user = current_user, course = course)

@student.route('/add_course', methods = ['GET','POST'])
@login_required
def add_course():
    course = session.query(Course).filter_by(name = request.form.get('name')).first()
    student = session.query(Student).filter_by(id = current_user.id).first()
    course.student.append(student)
    session.commit()
    return redirect(url_for('student.course', courseid = course.id))

@student.route('/other_courses')
@login_required
def other_courses():
    signed_up = session.query(Student_Course).filter_by(student_id = current_user.id).all()
    courses = session.query(Course).all()
    available = list()
    for i in courses:
        if i not in signed_up:
            available.append(i)
    return render_template('other_courses.html', user = current_user, courses = available)