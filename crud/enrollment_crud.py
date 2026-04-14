from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.enrollment import Enrollment


def enroll_student(session: Session, student_id: int, course_id: int) -> Enrollment | None:
    """Enroll a student in a course. Returns None if already enrolled."""
    existing = session.query(Enrollment).filter_by(
        student_id=student_id, course_id=course_id
    ).first()
    if existing:
        print(f"Student {student_id} is already enrolled in course {course_id}")
        return existing

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    session.add(enrollment)
    try:
        session.commit()
        session.refresh(enrollment)
        return enrollment
    except IntegrityError:
        session.rollback()
        return None


def update_progress(session: Session, student_id: int, course_id: int, progress: float) -> Enrollment | None:
    enrollment = session.query(Enrollment).filter_by(
        student_id=student_id, course_id=course_id
    ).first()
    if not enrollment:
        return None
    enrollment.progress = progress
    session.commit()
    session.refresh(enrollment)
    return enrollment


def get_student_enrollments(session: Session, student_id: int) -> list[Enrollment]:
    return session.query(Enrollment).filter(Enrollment.student_id == student_id).all()


def unenroll_student(session: Session, student_id: int, course_id: int) -> bool:
    enrollment = session.query(Enrollment).filter_by(
        student_id=student_id, course_id=course_id
    ).first()
    if not enrollment:
        return False
    session.delete(enrollment)
    session.commit()
    return True
