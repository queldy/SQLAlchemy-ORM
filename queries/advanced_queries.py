from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from models.user import User, UserProfile
from models.course import Course, Tag, course_tags
from models.enrollment import Enrollment


def get_user_with_profile(session: Session, user_id: int) -> User | None:
    """Eager-load user + profile (1:1)."""
    return (
        session.query(User)
        .options(joinedload(User.profile))
        .filter(User.id == user_id)
        .first()
    )


def get_courses_of_instructor(session: Session, instructor_id: int) -> list[Course]:
    """All courses taught by a given instructor (1:N)."""
    return (
        session.query(Course)
        .filter(Course.instructor_id == instructor_id)
        .options(joinedload(Course.tags))
        .all()
    )


def get_students_of_course(session: Session, course_id: int) -> list[User]:
    """All students enrolled in a specific course (N:N via Enrollment)."""
    return (
        session.query(User)
        .join(Enrollment, Enrollment.student_id == User.id)
        .filter(Enrollment.course_id == course_id)
        .all()
    )


def get_courses_by_tag(session: Session, tag_name: str) -> list[Course]:
    """Find all courses that have a specific tag (filter via N:N relation)."""
    return (
        session.query(Course)
        .join(course_tags, Course.id == course_tags.c.course_id)
        .join(Tag, Tag.id == course_tags.c.tag_id)
        .filter(Tag.name == tag_name.lower().strip())
        .all()
    )


def get_enrollments_with_details(session: Session, student_id: int):
    """
    JOIN query: student's enrollments with course title and instructor name.
    Returns list of dicts.
    """
    results = (
        session.query(
            Course.title.label("course_title"),
            User.username.label("instructor"),
            Enrollment.progress.label("progress"),
            Enrollment.enrolled_at.label("enrolled_at"),
        )
        .join(Enrollment, Enrollment.course_id == Course.id)
        .join(User, User.id == Course.instructor_id)
        .filter(Enrollment.student_id == student_id)
        .all()
    )
    return [
        {
            "course": r.course_title,
            "instructor": r.instructor,
            "progress": f"{r.progress:.1f}%",
            "enrolled_at": r.enrolled_at.strftime("%Y-%m-%d"),
        }
        for r in results
    ]


def get_course_stats(session: Session) -> list[dict]:
    """
    Complex aggregate query: course title + number of enrolled students + avg progress.
    """
    results = (
        session.query(
            Course.title,
            func.count(Enrollment.id).label("student_count"),
            func.avg(Enrollment.progress).label("avg_progress"),
        )
        .outerjoin(Enrollment, Enrollment.course_id == Course.id)
        .group_by(Course.id)
        .all()
    )
    return [
        {
            "course": r.title,
            "students": r.student_count,
            "avg_progress": f"{r.avg_progress or 0:.1f}%",
        }
        for r in results
    ]


def search_users_by_country(session: Session, country: str) -> list[User]:
    """Find users whose profile country matches (JOIN across 1:1)."""
    return (
        session.query(User)
        .join(UserProfile, UserProfile.user_id == User.id)
        .filter(UserProfile.country.ilike(f"%{country}%"))
        .all()
    )
