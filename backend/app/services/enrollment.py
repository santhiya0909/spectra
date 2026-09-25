from sqlalchemy.orm import Session

from app.db.models.academic import Subject, Enrollment


DEFAULT_SUBJECT_CODES = [
    "JAVA",
    "PYTHON",
    "DBMS",
    "STAT",
    "ECO",
]


def enroll_student_in_default_subjects(
    db: Session,
    student_id: int
):
    subjects = (
        db.query(Subject)
        .filter(Subject.code.in_(DEFAULT_SUBJECT_CODES))
        .all()
    )

    for subject in subjects:

        existing = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id == student_id,
                Enrollment.subject_id == subject.id
            )
            .first()
        )

        if not existing:
            enrollment = Enrollment(
                student_id=student_id,
                subject_id=subject.id
            )

            db.add(enrollment)

    db.commit()