from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), index=True, nullable=False)  # CHM101, PHY101, MTH101, BIO101
    question_text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_option = Column(String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    explanation = Column(Text, nullable=False, default="")


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)
    matric_number = Column(String(64), index=True, nullable=False)
    student_name = Column(String(120), nullable=False)
    started_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    current_course_index = Column(Integer, default=0, nullable=False)  # 0=CHM101, 1=PHY101, 2=MTH101, 3=BIO101
    gpa = Column(Float, nullable=True)
    total_correct = Column(Integer, nullable=True)
    total_questions = Column(Integer, default=140, nullable=False)

    sections = relationship(
        "CourseSectionAttempt",
        back_populates="attempt",
        cascade="all, delete-orphan",
        order_by="CourseSectionAttempt.course_order",
    )


class CourseSectionAttempt(Base):
    __tablename__ = "course_section_attempts"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("exam_attempts.id"), nullable=False, index=True)
    course_code = Column(String(20), nullable=False)
    course_order = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    credit_units = Column(Integer, default=2, nullable=False)

    started_at = Column(DateTime(timezone=True), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    is_submitted = Column(Boolean, default=False, nullable=False)

    score = Column(Integer, default=0, nullable=False)
    total_questions = Column(Integer, default=35, nullable=False)
    percentage = Column(Float, default=0.0, nullable=False)
    grade_letter = Column(String(2), nullable=True)
    grade_points = Column(Integer, nullable=True)

    attempt = relationship("ExamAttempt", back_populates="sections")
    answers = relationship(
        "AttemptAnswer",
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="AttemptAnswer.question_number",
    )


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("course_section_attempts.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    question_number = Column(Integer, nullable=False)  # 1..35 within the course
    selected_option = Column(String(1), nullable=True)  # 'A', 'B', 'C', 'D', or None
    is_flagged = Column(Boolean, default=False, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)

    section = relationship("CourseSectionAttempt", back_populates="answers")
    question = relationship("Question")
