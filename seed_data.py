from db.database import SessionLocal
from crud import (
    create_user, create_profile, get_or_create_user,
    create_course, enroll_student, update_progress,
)


def seed():
    session = SessionLocal()
    print("\n Seeding database with realistic data...\n")

    # ── Users ─────────────────────────────────────────────────────────────────
    alice, _ = get_or_create_user(session, "alice_dev", "alice@example.com", "securepass1")
    bob, _ = get_or_create_user(session, "bob_teaches", "bob@example.com", "securepass2")
    carol, _ = get_or_create_user(session, "carol_learns", "carol@example.com", "securepass3")
    dave, _ = get_or_create_user(session, "dave_codes", "dave@example.com", "securepass4")

    print(f"  👤 Users: {alice.username}, {bob.username}, {carol.username}, {dave.username}")

    # ── Profiles (1:1) ────────────────────────────────────────────────────────
    from crud.user_crud import create_profile
    from models.user import UserProfile
    from sqlalchemy import inspect

    def ensure_profile(session, user, full_name, bio, country, website):
        existing = session.query(UserProfile).filter_by(user_id=user.id).first()
        if existing:
            return existing
        return create_profile(session, user.id, full_name, bio, country, website)

    ensure_profile(session, alice, "Alice Petrova",
                   "Senior Python developer with 8 years of experience.",
                   "Russia", "https://alice.dev")
    ensure_profile(session, bob, "Bob Nazarov",
                   "Machine Learning engineer and educator.",
                   "Kazakhstan", "https://bobnazarov.io")
    ensure_profile(session, carol, "Carol Kim",
                   "Junior developer, passionate about web tech.",
                   "South Korea", "https://carolkim.dev")
    ensure_profile(session, dave, "Dave Omondi",
                   "Full-stack developer and open-source contributor.",
                   "Kenya", "https://daveomondi.com")

    print("   Profiles created (1:1 relationship)")

    # ── Courses (1:N) ─────────────────────────────────────────────────────────
    from models.course import Course

    def ensure_course(session, title, instructor_id, **kwargs):
        existing = session.query(Course).filter_by(title=title).first()
        if existing:
            return existing
        return create_course(session, title=title, instructor_id=instructor_id, **kwargs)

    c1 = ensure_course(session, "Python for Beginners", bob.id,
                       description="Learn Python from scratch with practical projects.",
                       price=29.99, language="English",
                       tag_names=["python", "beginner", "programming"])

    c2 = ensure_course(session, "Machine Learning with Scikit-Learn", bob.id,
                       description="Build real ML models using Python and scikit-learn.",
                       price=49.99, language="English",
                       tag_names=["python", "machine-learning", "data-science"])

    c3 = ensure_course(session, "Advanced SQLAlchemy ORM", alice.id,
                       description="Deep dive into SQLAlchemy: relationships, queries, migrations.",
                       price=39.99, language="English",
                       tag_names=["python", "database", "sqlalchemy", "backend"])

    c4 = ensure_course(session, "Web Development with FastAPI", alice.id,
                       description="Build modern REST APIs using FastAPI and SQLAlchemy.",
                       price=44.99, language="English",
                       tag_names=["python", "fastapi", "backend", "api"])

    print(f"   Courses: {c1.title}, {c2.title}, {c3.title}, {c4.title}")
    print("     (1:N — Alice and Bob are instructors with multiple courses)")

    # ── Enrollments (N:N) ─────────────────────────────────────────────────────
    enroll_student(session, carol.id, c1.id)
    enroll_student(session, carol.id, c2.id)
    enroll_student(session, carol.id, c3.id)
    enroll_student(session, dave.id, c1.id)
    enroll_student(session, dave.id, c4.id)
    enroll_student(session, alice.id, c2.id)  # Alice also takes Bob's ML course

    update_progress(session, carol.id, c1.id, 85.0)
    update_progress(session, carol.id, c2.id, 42.0)
    update_progress(session, carol.id, c3.id, 10.0)
    update_progress(session, dave.id, c1.id, 100.0)
    update_progress(session, dave.id, c4.id, 67.5)
    update_progress(session, alice.id, c2.id, 30.0)

    print("  🎓 Enrollments created (N:N with progress tracking)")
    print("\n Database seeded successfully!\n")

    session.close()


if __name__ == "__main__":
    from db.database import init_db
    init_db()
    seed()
