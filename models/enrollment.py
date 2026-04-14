from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from db.database import Base


class Enrollment(Base):
    """
    Represents a student enrolled in a course.
    Acts as the N:N association between User (student) and Course,
    with additional fields: enrolled_at and progress.
    """
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    progress = Column(Float, default=0.0)

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course"),
    )

    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    @validates("progress")
    def validate_progress(self, key, value):
        assert 0.0 <= value <= 100.0, "Progress must be between 0 and 100"
        return value

    def __repr__(self):
        return f"<Enrollment(student_id={self.student_id}, course_id={self.course_id}, progress={self.progress}%)>"
