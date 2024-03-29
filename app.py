from db import *
from auth import profile
from administrator import administrator
from professor import professor
from student import student
from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.register_blueprint(administrator)
app.register_blueprint(profile)
app.register_blueprint(professor)
app.register_blueprint(student)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    s = session.query(Student).filter_by(id = id).first()
    p = session.query(Professor).filter_by(id = id).first()
    a = session.query(Administrator).filter_by(id = id).first()
    if s is not None:
        return session.query(Student).filter_by(id = id).first()
    elif p is not None:
        return session.query(Professor).filter_by(id = id).first()
    elif a is not None:
        return session.query(Administrator).filter_by(id = id).first()
    else:
        return session.query(User).filter_by(id = id).first()

#app.run(port=5000)