import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

# association of the engine to the postgresql database in the pc
engine = create_engine('postgresql://postgres:gallina96!@localhost:5432/my-dbproj', echo=True)


Base = declarative_base()
# creation and binding of session
Session = sessionmaker(bind=engine)
session = Session()

# definition of the User superclass for teachers, students and administrators
class User(UserMixin, Base):
    __tablename__ = 'USERS'
    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    email_address = Column(String, unique = True)

    # class constructor
    def __init__(self, first_name, last_name, email_address, password):
        self.id = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password


# table that defines the many-to-many relationship between students and courses
#Student_Courses = Table('STUDENT_COURSES', Base.metadata, Column('COURSE_ID', ForeignKey('COURSES.id'), primary_key=True),
#                   Column('STUDENT_ID', ForeignKey('STUDENTS.id'), primary_key=True))


# inherits from users
class Student(User):
    __tablename__ = 'STUDENTS'
    id = Column(UUID(as_uuid=True), ForeignKey('USERS.id'), primary_key=true)

    #association proxy
    Course = association_proxy("student_course", "Course", creator = lambda Course:Student_Courses(Course=Course))

    # hierarchy mapping
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    # class constructor
    def __init__(self, first_name, last_name, email_address, password, Course = None):
        super().__init__(first_name, last_name, email_address, password)
        if Course:
            Course = Course


# inherits from users with
class Professor(User):
    __tablename__ = 'PROFESSOR'
    id = Column(UUID(as_uuid=True), ForeignKey('USERS.id'), primary_key=true)
    

    # hierarchy mapping
    __mapper_args__ = {
        'polymorphic_identity': 'professor'
    }

    # class constructor
    def __init__(self, first_name, last_name, email_address, password):
        super().__init__(first_name, last_name, email_address, password)


class Course(Base):
    __tablename__ = 'COURSES'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, unique = True)
    description = Column(String)

    # many to 1 relationship with professor
    professor_id = Column(UUID(as_uuid=True), ForeignKey("PROFESSOR.id"))
    Professor = relationship(Professor, backref='Courses')

    # many-to-many relationship with students
    #Student = relationship(Student, secondary=Student_Courses, backref='Courses')

    #association proxy
    Student = association_proxy("course_student", "Student", creator = lambda Student:Student_Courses(Student=Student))

    # class constructor
    def __init__(self, name, description, professor, Student = None):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.professor_id = professor
        if Student:
            Student = Student


class Lectures(Base):
    __tablename__ = 'LECTURES'

    id = Column(UUID(as_uuid=True), primary_key=True)
    date = Column(Date)
    mode = Column(String)
    classroom = Column(String)

    # many to 1 relationship with courses
    course_id = Column(UUID(as_uuid=True), ForeignKey("COURSES.id"))
    Course = relationship(Course, backref='Lectures')

    # class constructor
    def __init__(self, date, mode, classroom):
        self.id = uuid.uuid4()
        self.date = date
        self.mode = mode
        self.classroom = classroom

# inherits from users with
class Administrator(User):
    __tablename__ = 'ADMINISTRATOR'
    id = Column(UUID(as_uuid=True), ForeignKey('USERS.id'), primary_key=true)
    

    # hierarchy mapping
    __mapper_args__ = {
        'polymorphic_identity': 'administrator'
    }

    # class constructor
    def __init__(self, first_name, last_name, email_address, password):
        super().__init__(first_name, last_name, email_address, password)

class Class(Base):
    __tablename__ = 'CLASS'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, unique = True)
    capacity = Column(Integer)

    # class constructor
    def __init__(self, name, capacity):
        self.id = uuid.uuid4()
        self.name = name
        self.capacity = capacity


class Student_Courses(Base):
    __tablename__ = 'STUDENT_COURSES'
    course_id = Column('COURSE_ID', UUID(as_uuid=True), ForeignKey('COURSES.id'), primary_key=True)
    student_id = Column('STUDENT_ID', UUID(as_uuid=True), ForeignKey('STUDENTS.id'), primary_key=True)

    Course = relationship(Course, backref = "course_student")
    Student = relationship(Student, backref = "student_course")

    def __init__(self, Student = None, Course = None):
        self.Student = Student
        self.Course = Course


    #def __init__(self, proxied=None):
    #    if type(proxied) is Course:
    #        self.Course = proxied
    #    elif type(proxied) is Student:
    #        self.Student = proxied


def init_db():
    Base.metadata.create_all(engine)


init_db()