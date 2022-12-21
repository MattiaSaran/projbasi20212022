from flask import Blueprint
from db import *
from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user

profile = Blueprint('profile', __name__)

@profile.route('/')
def home():
    return render_template('login.html')

@profile.route('/login', methods=['GET', 'POST'])
def login():
    conn = engine.connect()
    u = session.query(User).filter_by(email_address = request.form.get('email_address')).first()
    s = session.query(Student).filter_by(id = u.id).first()
    p = session.query(Professor).filter_by(id = u.id).first()
    a = session.query(Administrator).filter_by(id = u.id).first()
    conn.close()
    if u is not None and request.form.get('password') == u.password:
        if s is not None:
            login_user(u)
            return redirect(url_for('student.page'))
        elif p is not None:
            login_user(u)
            return redirect(url_for('professor.page'))
        elif a is not None:
            login_user(u)
            return redirect(url_for('administrator.page'))
        else:
            return null
    else:
        return redirect(url_for('profile.home'))

@profile.route('/registration')
def registration():
    return render_template('registration.html')

@profile.route('/adduser', methods = ['POST'])
def adduser():
    if(request.form.get('role') == 'student'):
        user = Student(request.form.get('first_name'), request.form.get('last_name'), request.form.get('email_address'), request.form.get('password'))
        print(user)
        session.add(user)
        session.commit()
        return redirect(url_for('profile.home'))
    elif(request.form.get('role') == 'professor'):
        user = Professor(request.form.get('first_name'), request.form.get('last_name'), request.form.get('email_address'), request.form.get('password'))
        session.add(user)
        session.commit()
        return redirect(url_for('profile.home'))
    elif(request.form.get('role') == 'administrator'):
        user = Professor(request.form.get('first_name'), request.form.get('last_name'), request.form.get('email_address'), request.form.get('password'))
        session.add(user)
        session.commit()
        return redirect(url_for('profile.home'))
    else:
        return redirect(url_for('profile.home'))

@profile.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('profile.home'))