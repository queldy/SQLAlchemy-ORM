import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from db.database import init_db, SessionLocal
from seed_data import seed
import crud
import queries


def separator(title: str):
    print(f"\n{'═' * 55}")
    print(f"  {title}")
    print('═' * 55)


def run_demo():
    separator("STEP 1: Initialize Database")
    init_db()

    separator("STEP 2: Seed Data")
    seed()

    session = SessionLocal()

    separator("STEP 3: CRUD Operations on User")

    new_user, created = crud.get_or_create_user(
        session, "eve_analyst", "eve@example.com", "mypassword"
    )
    print(f"  CREATE: {'Created' if created else 'Found'} user → {new_user}")
    crud.create_profile(session, new_user.id, "Eve Sato",
                        bio="Data analyst from Japan.",
                        country="Japan", website="https://evesato.jp") if created else None

    found = crud.get_user_by_id(session, new_user.id)
    print(f"  READ by ID: {found}")

    found_by_email = crud.get_user_by_email(session, "eve@example.com")
    print(f"  READ by email: {found_by_email}")

    updated = crud.update_user_email(session, new_user.id, "eve_updated@example.com")
    print(f"  UPDATE email: {updated}")

    deleted = crud.delete_user(session, new_user.id)
    print(f"  DELETE user (id={new_user.id}): {'success!' if deleted else 'failed'}")

    separator("STEP 4: Queries — Search by ID & Field")

    alice = crud.get_user_by_username(session, "alice_dev")
    bob = crud.get_user_by_username(session, "bob_teaches")
    carol = crud.get_user_by_username(session, "carol_learns")

    print(f"  Search user by username 'alice_dev': {alice}")

    course = crud.get_course_by_title(session, "Python")
    print(f"  Search course by title 'Python': {course}")

    separator("STEP 5: Queries — Using Relationships")

    user_with_profile = queries.get_user_with_profile(session, bob.id)
    print(f"\n  1:1 User + Profile:")
    print(f"    User: {user_with_profile.username}")
    print(f"    Profile: {user_with_profile.profile.full_name} | {user_with_profile.profile.country}")

    bob_courses = queries.get_courses_of_instructor(session, bob.id)
    print(f"\n  1:N Courses by instructor '{bob.username}':")
    for c in bob_courses:
        tags = [t.name for t in c.tags]
        print(f"{c.title} | ${c.price} | tags: {tags}")

    students = queries.get_students_of_course(session, bob_courses[0].id)
    print(f"\n  N:N Students in course '{bob_courses[0].title}':")
    for s in students:
        print(f"{s.username} ({s.email})")

    python_courses = queries.get_courses_by_tag(session, "python")
    print(f"\n  Filter — Courses tagged 'python':")
    for c in python_courses:
        print(f"{c.title}")

    enrollment_details = queries.get_enrollments_with_details(session, carol.id)
    print(f"\n  JOIN — Enrollments for '{carol.username}':")
    for e in enrollment_details:
        print(f"{e['course']} | Instructor: {e['instructor']} | Progress: {e['progress']}")

    stats = queries.get_course_stats(session)
    print(f"\n  AGGREGATE — Course statistics:")
    for s in stats:
        print(f"{s['course']}: {s['students']} students, avg progress {s['avg_progress']}")

    kazakh_users = queries.search_users_by_country(session, "Kazakhstan")
    print(f"\n  JOIN (1:1) — Users from Kazakhstan:")
    for u in kazakh_users:
        print(f"{u.username} — {u.profile.full_name}")

    separator("ALL DEMONSTRATIONS COMPLETED")
    session.close()


if __name__ == "__main__":
    run_demo()
