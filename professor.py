from db import *
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask import Blueprint

professor = Blueprint('professor', __name__, url_prefix='/professor')

@professor.route('/', methods=['GET'])
@login_required
def page():
    courses = session.query(Course).filter_by(professor_id = current_user.id).all()
    return render_template('professor.html', user = current_user, courses = courses)

@professor.route('/<course>')
@login_required
def course(course):
    return render_template('professor_course.html', user = current_user, course = course)

@professor.route('/new_course')
@login_required
def new_course():
    return render_template('create_course.html', user = current_user)

@professor.route('/create_course', methods = ['POST'])
@login_required
def create_course():
    course = Course(request.form.get('name'), request.form.get('description'), current_user.id)
    session.add(course)
    session.commit()
    return redirect(url_for('professor.course', user = current_user, course = course))

@professor.route('/new_lecture/<course>')
@login_required
def new_lecture(course):
    return render_template('new_lecture.html', course = course)

@professor.route('/add_lecture/<course>', methods = ['POST'])
@login_required
def add_lecture(course):
    lecture = Lectures(request.form.get('date'), request.form.get('mode'), request.form.get('classroom'))
    session.add(lecture)
    session.commit()
    return redirect(url_for('professor.course', user = current_user, course = course))

@professor.route('/update/<lecture>')
@login_required
def update_lecture(lecture):
    return render_template('update_lecture.html', lecture = lecture)

@professor.route('/update/<course>')
@login_required
def update_course(course):
    return render_template('update_course.html', course = course)

@professor.route('/modify/<lecture>', methods = ['GET', 'POST'])
@login_required
def modify_lecture(lecture):
    session.query(Lectures).filter_by(id = lecture.id).first()
    update({Lectures.date:request.form.get('date'), Lectures.mode:request.form.get('mode'), Lectures.classroom:request.form.get('classroom')}, synchronize_session = False)
    session.commit()

@professor.route('/modify/<course>', methods = ['GET', 'POST'])
@login_required
def modify_course(course):
    session.query(Course).filter_by(id = course.id).first()
    update({Course.name:request.form.get('name'), Course.capacity:request.form.get('capacity')}, synchronize_session = False)
    session.commit()