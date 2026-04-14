from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from db.database import Base

course_tags = Table(
    "course_tags",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), default="")
    price = Column(Float, default=0.0)
    language = Column(String(30), default="English")
    created_at = Column(DateTime, default=datetime.utcnow)

    instructor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    instructor = relationship("User", back_populates="courses_taught")

    tags = relationship("Tag", secondary=course_tags, back_populates="courses")

    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    @validates("price")
    def validate_price(self, key, value):
        assert value >= 0, "Price cannot be negative"
        return value

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', price={self.price})>"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    courses = relationship("Course", secondary=course_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"
