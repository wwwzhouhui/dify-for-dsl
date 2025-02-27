from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True)
    student_name = Column(String(50), nullable=False)
    gender = Column(String(1))
    class_name = Column(String(20))
    admission_date = Column(Date)
    
    scores = relationship('Score', back_populates='student')

class Course(Base):
    __tablename__ = 'courses'
    
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(50), nullable=False)
    credit = Column(Float(precision=3))
    
    scores = relationship('Score', back_populates='course')

class Score(Base):
    __tablename__ = 'scores'
    
    score_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    score = Column(Float(precision=5))
    exam_date = Column(Date)
    
    student = relationship('Student', back_populates='scores')
    course = relationship('Course', back_populates='scores')