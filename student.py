from db import *
from flask import render_template, request, flash, redirect, url_for
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
    lectures = session.query(Lecture).filter_by(course_id = courseid).all()
    return render_template('student_course.html', user = current_user, course = course, lectures = lectures)

@student.route('/reserve_seat/<lecture>')
@login_required
def reserve_seat(lecture):
    l = session.query(Lecture).filter_by(id = lecture).first()
    if(l.mode != 'online' and l.seats > 0 and current_user.id not in l.students):
        l.seats = l.seats - 1
        l.students.append(current_user.id)
        session.commit()
    elif(current_user.id in l.students):
        flash('lezione già prenotata')
    return redirect(url_for('student.course', courseid = l.course_id))

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
    if signed_up is not None:
        c = list()
        for i in signed_up:
            c.append(session.query(Course).filter_by(id = i.course_id).first())
    else:
        c = None
    courses = session.query(Course).all()
    available = list()
    for i in courses:
        if i not in c:
            available.append(i)
    return render_template('other_courses.html', user = current_user, courses = available)