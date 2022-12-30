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
    __tablename__ = 'USER'
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

class Student(User):
    __tablename__="STUDENT"
    # PK column and tablename etc. come from the mixin
    id = Column(UUID(as_uuid=True), ForeignKey('USER.id'), primary_key=true)
    # association proxy
    course = association_proxy('student_course', 'COURSE', creator=lambda course: Student_Course(course=course))

    # hierarchy mapping
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, first_name, last_name, email_address, password, course = None):
        super().__init__(first_name, last_name, email_address, password)
        if course:
            self.course = course

# inherits from users with
class Professor(User):
    __tablename__ = 'PROFESSOR'
    id = Column(UUID(as_uuid=True), ForeignKey('USER.id'), primary_key=true)
    

    # hierarchy mapping
    __mapper_args__ = {
        'polymorphic_identity': 'professor'
    }

    # class constructor
    def __init__(self, first_name, last_name, email_address, password):
        super().__init__(first_name, last_name, email_address, password)


class Course(Base):
    __tablename__="COURSE"
    # PK column and tablename etc. come from the mixin
    id = Column(UUID(as_uuid=True), primary_key=true)
    name = Column(String, unique = True)
    description = Column(String)

    # association proxy
    student = association_proxy('course_student', 'STUDENT', creator=lambda student: Student_Course(student=student))

    # many to 1 relationship with professor
    professor_id = Column(UUID(as_uuid=True), ForeignKey("PROFESSOR.id"))
    professor = relationship(Professor, backref='Course')

    def __init__(self, name, description, professor, student=None):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.professor_id = professor
        if student:
            self.student = student

class Lecture(Base):
    __tablename__ = 'LECTURE'

    id = Column(UUID(as_uuid=True), primary_key=True)
    date = Column(Date)
    mode = Column(String)
    classroom = Column(String)

    # many to 1 relationship with courses
    course_id = Column(UUID(as_uuid=True), ForeignKey("COURSE.id"))
    course = relationship(Course, backref='lecture')

    # class constructor
    def __init__(self, date, mode, classroom):
        self.id = uuid.uuid4()
        self.date = date
        self.mode = mode
        self.classroom = classroom

# inherits from users with
class Administrator(User):
    __tablename__ = 'ADMINISTRATOR'
    id = Column(UUID(as_uuid=True), ForeignKey('USER.id'), primary_key=true)
    

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


class Student_Course(Base):

    __tablename__ = "STUDENT_COURSE"
    course_id = Column("course_id",
        UUID(as_uuid=True), ForeignKey("COURSE.id"), primary_key=True)
    student_id = Column("student_id",
        UUID(as_uuid=True), ForeignKey("STUDENT.id"), primary_key=True)
    # relations
    course = relationship(
        "Course",
        backref="course_student",
        cascade="all, delete-orphan",
        single_parent=True)
    student = relationship(
        "Student",
        backref="student_course",
        cascade="all, delete-orphan",
        single_parent=True)

    def __init__(self, course=None, student=None):
        self.course = course
        self.student = student


def init_db():
    Base.metadata.create_all(engine)


init_db()

#prof = Professor("Prof", "1", "prof@unive.it", "password")

#session.add(prof)
#session.add(Student("Stud", "1", "stud@unive.it", "password"))
#session.add(Course("ASD", "Corso", prof.id))
#session.commit()

#student = session.query(Student).first()
#course = session.query(Course).first()
#course.student.append(student)
#session.commit()