from db import *
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask import Blueprint

administrator = Blueprint('administrator', __name__, url_prefix='/administrator')

@administrator.route('/', methods=['GET'])
@login_required
def page():
    classes = session.query(Class).all()
    return render_template('administrator.html', user = current_user, classes = classes)

@administrator.route('/create_class', methods=['GET'])
@login_required
def create_class():
    return render_template('new_room.html', user = current_user)

@administrator.route('/add_class', methods = ['POST'])
@login_required
def add_class():
    c = Class(request.form.get('name'), request.form.get('capacity'))
    session.add(c)
    session.commit()
    return redirect(url_for('administrator.page'))