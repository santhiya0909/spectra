from app.db.database import SessionLocal
from app.db.models.academic import Subject


DEFAULT_SUBJECTS = [
    {
        "name": "Java Programming",
        "code": "JAVA",
        "description": "Learn Java programming, object-oriented programming, inheritance, exceptions and more."
    },
    {
        "name": "Python Programming",
        "code": "PYTHON",
        "description": "Learn Python fundamentals, functions, object-oriented programming and problem solving."
    },
    {
        "name": "Database Management Systems",
        "code": "DBMS",
        "description": "Learn SQL, database design, normalization, transactions and database management."
    },
    {
        "name": "Statistics",
        "code": "STAT",
        "description": "Learn probability, distributions, statistical analysis and data interpretation."
    },
    {
        "name": "Economics",
        "code": "ECO",
        "description": "Learn demand, supply, pricing, costing and fundamental economic concepts."
    }
]


def seed_subjects():
    db = SessionLocal()

    try:
        for subject_data in DEFAULT_SUBJECTS:
            existing = (
                db.query(Subject)
                .filter(Subject.code == subject_data["code"])
                .first()
            )

            if not existing:
                subject = Subject(**subject_data)
                db.add(subject)
                print(f"Added subject: {subject_data['name']}")
            else:
                print(f"Already exists: {subject_data['name']}")

        db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    seed_subjects()
    print("Default subjects setup completed.")
    try:
        from scripts.seed_full_curriculum import seed_database_curriculum
        seed_database_curriculum()
        print("Full curriculum seeding completed.")
    except Exception as e:
        print(f"Curriculum seeding error: {e}")

    from scripts.seed_curriculum import seed_curriculum_data
    seed_curriculum_data()
    print("Complete curriculum setup completed.")