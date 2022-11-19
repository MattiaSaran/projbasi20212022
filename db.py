import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# association of the engine to the postgresql database in the pc
engine = create_engine('postgresql://postgres:gallina96!@localhost:5432/my-dbproj', echo=True)


Base = declarative_base()
# creation and binding of session
Session = sessionmaker(bind=engine)
session = Session()

# definition of the User superclass for teachers and students
class User(Base):
    __tablename__ = 'USERS'
    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    email_address = Column(String)

    # class constructor
    def __init__(self, first_name, last_name, email_address, password):
        self.id = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password


# table that defines the many-to-many relationship between students and courses
Student_Courses = Table('STUDENT_COURSES', Base.metadata, Column('COURSE_ID', ForeignKey('COURSES.id'), primary_key=True),
                   Column('STUDENT_ID', ForeignKey('STUDENTS.id'), primary_key=True))


# inherits from users
class Student(User):
    __tablename__ = 'STUDENTS'
    id = Column(UUID(as_uuid=True), ForeignKey('USERS.id'), primary_key=true)

    # hierarchy mapping
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    # class constructor
    def __init__(self, first_name, last_name, email_address, password):
        super().__init__(first_name, last_name, email_address, password)


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
    name = Column(String)
    capacity = Column(Integer)

    # many to 1 relationship with professor
    professor_id = Column(UUID(as_uuid=True), ForeignKey("PROFESSOR.id"))
    Professor = relationship(Professor, backref='Course')

    # many-to-many relationship with students
    Student = relationship(Student, secondary=Student_Courses, back_populates='Course')

    # class constructor
    def __init__(self, name, capacity):
        self.id = uuid.uuid4()
        self.name = name
        self.capacity = capacity


# many-to-many relationship between students and courses
Student.Course = relationship(Course, secondary=Student_Courses, back_populates='Student')


class Lectures(Base):
    __tablename__ = 'LECTURES'

    id = Column(UUID(as_uuid=True), primary_key=True)
    date = Column(Date)
    mode = Column(String)
    classroom = Column(String)

    # many to 1 relationship with courses
    course_id = Column(UUID(as_uuid=True), ForeignKey("COURSES.id"))
    Course = relationship(Course, back_populates='Lectures')

    # class constructor
    def __init__(self, date, mode, classroom):
        self.id = uuid.uuid4()
        self.date = date
        self.mode = mode
        self.classroom = classroom


# 1 to many relationship with lectures
Course.Lectures = relationship(Lectures, order_by=Lectures.id, back_populates='Course')


def init_db():
    Base.metadata.create_all(engine)


init_db()