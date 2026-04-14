from sqlalchemy.orm import Session
from models.course import Course, Tag


def get_or_create_tag(session: Session, name: str) -> tuple[Tag, bool]:
    tag = session.query(Tag).filter(Tag.name == name.lower().strip()).first()
    if tag:
        return tag, False
    tag = Tag(name=name.lower().strip())
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag, True


def create_course(session: Session, title: str, instructor_id: int,
                  description: str = "", price: float = 0.0,
                  language: str = "English", tag_names: list[str] = None) -> Course:
    course = Course(
        title=title,
        instructor_id=instructor_id,
        description=description,
        price=price,
        language=language,
    )
    if tag_names:
        for tag_name in tag_names:
            tag, _ = get_or_create_tag(session, tag_name)
            course.tags.append(tag)
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def get_course_by_id(session: Session, course_id: int) -> Course | None:
    return session.query(Course).filter(Course.id == course_id).first()


def get_course_by_title(session: Session, title: str) -> Course | None:
    return session.query(Course).filter(Course.title.ilike(f"%{title}%")).first()


def get_all_courses(session: Session) -> list[Course]:
    return session.query(Course).all()


def get_courses_by_instructor(session: Session, instructor_id: int) -> list[Course]:
    return session.query(Course).filter(Course.instructor_id == instructor_id).all()


def update_course_price(session: Session, course_id: int, new_price: float) -> Course | None:
    course = get_course_by_id(session, course_id)
    if not course:
        return None
    course.price = new_price
    session.commit()
    session.refresh(course)
    return course


def add_tag_to_course(session: Session, course_id: int, tag_name: str) -> Course | None:
    course = get_course_by_id(session, course_id)
    if not course:
        return None
    tag, _ = get_or_create_tag(session, tag_name)
    if tag not in course.tags:
        course.tags.append(tag)
        session.commit()
    return course


def delete_course(session: Session, course_id: int) -> bool:
    course = get_course_by_id(session, course_id)
    if not course:
        return False
    session.delete(course)
    session.commit()
    return True
