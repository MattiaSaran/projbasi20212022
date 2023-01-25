import datetime
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

@professor.route('/<courseid>')
@login_required
def course(courseid):
    course = session.query(Course).filter_by(id = courseid).first()
    lectures = session.query(Lecture).filter_by(course_id = courseid).all()
    return render_template('professor_course.html', user = current_user, course = course, lectures = lectures)

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
    return redirect(url_for('professor.course', courseid = course.id))

@professor.route('/new_lecture/<courseid>')
@login_required
def new_lecture(courseid):
    classroom = session.query(Class).all()
    return render_template('new_lecture.html', course = courseid, classroom = classroom)

@professor.route('/new_lecture/<courseid>', methods = ['POST'])
@login_required
def new_lecture2(courseid):
    mode = request.form.get('mode')
    if(mode == 'online'):
        time = create_slots()
        slots = list()
        for i in time:
            slots.append(i.strftime('%m/%d/%y %H:%M'))
        return render_template('new_lecture_online.html', course = courseid, slots = slots, mode = mode)
    else:
        classroom = session.query(Class).all()
        return render_template('new_lecture_presenza.html', course = courseid, mode = mode, classroom = classroom)

@professor.route('/new_lecture/<courseid>', methods = ['POST'])
@login_required
def new_lecture_orari(courseid):
    classroom = session.query(Class).all()
    return render_template('new_lecture_orari.html', course = courseid, classroom = classroom)

@professor.route('/new_lecture/<courseid>', methods = ['POST'])
@login_required
def new_lecture_presenza(courseid):
    classroom = session.query(Class).all()
    return render_template('new_lecture.html', course = courseid, classroom = classroom)

@professor.route('/add_lecture/<courseid>/<mode>/<classroom>', methods = ['POST'])
@login_required
def add_lecture(courseid, mode, classroom):
    date = datetime.datetime.strptime(request.form.get('slots'), '%m/%d/%y %H:%M')
    lecture = Lecture(date, mode, classroom, courseid)
    if(mode != 'online'):
        if(date not in classroom.slots):
            return redirect(url_for('professor.new_lecture', courseid))
        else:
            classroom.slots.remove(date)
            session.add(lecture)
            session.commit()
            return redirect(url_for('professor.course', courseid = courseid))
    else:
        session.add(lecture)
        session.commit()
        return redirect(url_for('professor.course', courseid = courseid))

@professor.route('/update/<lectureid>')
@login_required
def update_lecture(lectureid):
    lecture = session.query(Course).filter_by(id = lectureid).all()
    return render_template('update_lecture.html', lecture = lecture)

@professor.route('/update/<courseid>')
@login_required
def update_course(courseid):
    course = session.query(Course).filter_by(id = courseid).all()
    return render_template('update_course.html', course = course)

@professor.route('/modify/<lectureid>', methods = ['GET', 'POST'])
@login_required
def modify_lecture(lectureid):
    session.query(Lecture).filter_by(id = lectureid).first()
    update({Lecture.date:request.form.get('date'), Lecture.mode:request.form.get('mode'), Lecture.classroom:request.form.get('classroom')}, synchronize_session = False)
    session.commit()

@professor.route('/modify/<courseid>', methods = ['GET', 'POST'])
@login_required
def modify_course(courseid):
    course = session.query(Course).filter_by(id = courseid).all()
    session.query(Course).filter_by(id = course.id).first()
    update({Course.name:request.form.get('name'), Course.capacity:request.form.get('capacity')}, synchronize_session = False)
    session.commit()