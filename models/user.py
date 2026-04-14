from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    courses_taught = relationship("Course", back_populates="instructor", cascade="all, delete-orphan")

    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")

    @validates("email")
    def validate_email(self, key, value):
        assert "@" in value, "Invalid email address"
        return value.lower().strip()

    @validates("username")
    def validate_username(self, key, value):
        assert len(value) >= 3, "Username must be at least 3 characters"
        return value.strip()

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    bio = Column(String(500), default="")
    avatar_url = Column(String(255), default="")
    country = Column(String(60), default="")
    website = Column(String(255), default="")

    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, full_name='{self.full_name}')>"
