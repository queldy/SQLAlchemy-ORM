from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import User, UserProfile


def create_user(session: Session, username: str, email: str, password: str) -> User:
    user = User(username=username, email=email, hashed_password=f"hashed_{password}")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_profile(session: Session, user_id: int, full_name: str, bio: str = "",
                   country: str = "", website: str = "") -> UserProfile:
    profile = UserProfile(
        user_id=user_id,
        full_name=full_name,
        bio=bio,
        country=country,
        website=website,
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def get_or_create_user(session: Session, username: str, email: str, password: str) -> tuple[User, bool]:
    """Returns (user, created). If user exists — returns existing one."""
    user = session.query(User).filter_by(email=email).first()
    if user:
        return user, False
    user = create_user(session, username, email, password)
    return user, True


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email.lower().strip()).first()


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.query(User).filter(User.username == username).first()


def get_all_users(session: Session) -> list[User]:
    return session.query(User).all()


def update_user_email(session: Session, user_id: int, new_email: str) -> User | None:
    user = get_user_by_id(session, user_id)
    if not user:
        return None
    user.email = new_email
    session.commit()
    session.refresh(user)
    return user


def update_profile(session: Session, user_id: int, **kwargs) -> UserProfile | None:
    profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        return None
    for field, value in kwargs.items():
        if hasattr(profile, field):
            setattr(profile, field, value)
    session.commit()
    session.refresh(profile)
    return profile


def delete_user(session: Session, user_id: int) -> bool:
    user = get_user_by_id(session, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True
