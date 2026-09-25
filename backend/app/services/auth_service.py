from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.user import (
    User,
    StudentProfile,
    TeacherProfile,
    AuditLog,
)

from app.db.models.academic import (
    Subject,
    Enrollment,
)

from app.schemas.auth import (
    UserRegister,
    Token,
)

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)


# ============================================================
# AUTHENTICATE USER
# ============================================================

def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> Optional[User]:
    """
    Verify user credentials and return the user.
    Returns None when credentials are invalid.
    """

    user = (
        db.query(User)
        .filter(
            User.email == email.lower().strip()
        )
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user


# ============================================================
# REGISTER USER
# ============================================================

def register_user(
    db: Session,
    user_in: UserRegister,
) -> User:
    """
    Create a new user account and create
    the appropriate student/teacher profile.
    """

    # Check whether email already exists
    existing = (
        db.query(User)
        .filter(
            User.email == user_in.email.lower().strip()
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    # --------------------------------------------------------
    # Create user
    # --------------------------------------------------------

    hashed_pw = get_password_hash(
        user_in.password
    )

    user = User(
        name=user_in.name.strip(),
        email=user_in.email.lower().strip(),
        password_hash=hashed_pw,
        role=user_in.role,
    )

    db.add(user)
    db.flush()

    # --------------------------------------------------------
    # STUDENT
    # --------------------------------------------------------

    if user.role == "STUDENT":

        student_id = (
            user_in.student_id
            or f"STU-{user.id:04d}"
        )

        profile = StudentProfile(
            user_id=user.id,
            student_id=student_id,
            department=(
                user_in.department
                or "Computer Science"
            ),
            semester=(
                user_in.semester
                or 4
            ),
            academic_year="2025-2026",
        )

        db.add(profile)
        db.flush()

        # ----------------------------------------------------
        # Default Spectra subjects
        # ----------------------------------------------------

        default_subject_codes = [
            "JAVA",
            "PYTHON",
            "DBMS",
            "STAT",
            "ECO",
        ]

        subjects = (
            db.query(Subject)
            .filter(
                Subject.code.in_(
                    default_subject_codes
                )
            )
            .all()
        )

        # ----------------------------------------------------
        # Enroll student in subjects
        # ----------------------------------------------------

        for subject in subjects:

            existing_enrollment = (
                db.query(Enrollment)
                .filter(
                    Enrollment.student_id == profile.id,
                    Enrollment.subject_id == subject.id,
                )
                .first()
            )

            if not existing_enrollment:

                enrollment = Enrollment(
                    student_id=profile.id,
                    subject_id=subject.id,
                )

                db.add(enrollment)

    # --------------------------------------------------------
    # TEACHER
    # --------------------------------------------------------

    elif user.role == "TEACHER":

        employee_id = (
            user_in.employee_id
            or f"TCH-{user.id:04d}"
        )

        profile = TeacherProfile(
            user_id=user.id,
            employee_id=employee_id,
            department=(
                user_in.department
                or "Computer Science & Engineering"
            ),
        )

        db.add(profile)

    # --------------------------------------------------------
    # AUDIT LOG
    # --------------------------------------------------------

    audit = AuditLog(
        user_id=user.id,
        action="USER_REGISTERED",
        entity="USER",
        entity_id=str(user.id),
    )

    db.add(audit)

    # --------------------------------------------------------
    # Save changes
    # --------------------------------------------------------

    db.commit()
    db.refresh(user)

    return user


# ============================================================
# CREATE USER TOKEN
# ============================================================

def create_user_token(
    user: User,
) -> Token:
    """
    Generate JWT token response for the user.
    """

    access_token = create_access_token(
        subject=user.id,
        role=user.role,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        name=user.name,
        email=user.email,
    )