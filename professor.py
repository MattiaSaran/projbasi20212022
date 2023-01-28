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

@professor.route('/lecture/<lecture>', methods=['GET'])
@login_required
def lecture(lecture):
    l = session.query(Lecture).filter_by(id = lecture).first()
    students = list()
    for i in l.students:
        students.append(session.query(User).filter_by(id = i).first())
    return render_template('lecture.html', lecture = l, students = students)

@professor.route('/<courseid>')
@login_required
def course(courseid):
    course = session.query(Course).filter_by(id = courseid).first()
    s_id = session.query(Student_Course).filter_by(course_id = courseid).all()
    count = 0
    if s_id is not None:
        students = list()
        for i in s_id:
            count = count + 1
            students.append(session.query(Student).filter_by(id = i.student_id).first())
    else:
        students = None
    lectures = session.query(Lecture).filter_by(course_id = courseid).all()
    return render_template('professor_course.html', user = current_user, course = course, lectures = lectures, students = students, count = count)


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
    return render_template('new_lecture.html', course = courseid)

@professor.route('/new_lecture2/<courseid>', methods = ['POST'])
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
        c = session.query(Class).all()
        classroom = list()
        for i in c:
            classroom.append(i.name)
        return render_template('new_lecture_presenza.html', course = courseid, mode = mode, classroom = classroom)

@professor.route('/new_lecture_presenza/<courseid>/<mode>', methods = ['POST'])
@login_required
def new_lecture_presenza(courseid, mode):
    classroom = request.form.get('classroom')
    c = session.query(Class).filter_by(name = classroom).first()
    slots = list()
    for i in c.slots:
        slots.append(i.strftime('%m/%d/%y %H:%M'))
    return render_template('new_lecture_orari.html', course = courseid, classroom = classroom, mode = mode, slots = slots)

@professor.route('/add_lecture/<courseid>/<mode>/<classroom>', methods = ['POST'])
@login_required
def add_lecture(courseid, mode, classroom):
    date = datetime.datetime.strptime(request.form.get('slots'), '%m/%d/%y %H:%M')
    if(mode != 'online'):
        c = session.query(Class).filter_by(name = classroom).first()
        lecture = Lecture(date, mode, classroom, courseid, c.capacity)
        if(date not in c.slots):
            return redirect(url_for('professor.new_lecture', courseid))
        else:
            c.slots.remove(date)
            session.add(lecture)
            session.commit()
            return redirect(url_for('professor.course', courseid = courseid))
    else:
        lecture = Lecture(date, mode, classroom, courseid, 0)
        session.add(lecture)
        session.commit()
        return redirect(url_for('professor.course', courseid = courseid))

@professor.route('/delete_lecture/<lectureid>/<courseid>')
@login_required
def delete_lecture(lectureid, courseid):
    lecture = session.query(Lecture).filter_by(id = lectureid).first()
    if(lecture.mode != 'online'):
        classroom = session.query(Class).filter_by(name = lecture.classroom).first()
        classroom.slots.append(lecture.date)
        classroom.slots.sort()
        session.commit()
    session.delete(lecture)
    session.commit()
    return redirect(url_for('professor.course', courseid = courseid))