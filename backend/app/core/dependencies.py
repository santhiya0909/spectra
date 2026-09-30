from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import decode_access_token
from app.db.models.user import User, StudentProfile, TeacherProfile

security_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Extract and validate the currently authenticated user from Bearer JWT token."""
    if not auth_credentials or not auth_credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token subject invalid.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format in token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with token no longer exists.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def get_optional_current_user(
    auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Extract and validate the currently authenticated user if token present, else None."""
    if not auth_credentials or not auth_credentials.credentials:
        return None

    token = auth_credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        return None

    user_id_str = payload.get("sub")
    if not user_id_str:
        return None

    try:
        user_id = int(user_id_str)
    except ValueError:
        return None

    return db.query(User).filter(User.id == user_id).first()

def require_role(allowed_roles: List[str]):
    """RBAC dependency ensuring the user has one of the allowed roles."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: requires one of {allowed_roles}, your role is {current_user.role}.",
            )
        return current_user
    return role_checker

def get_current_student(
    current_user: User = Depends(require_role(["STUDENT", "ADMIN"])),
    db: Session = Depends(get_db)
) -> StudentProfile:
    """Retrieve the StudentProfile for the current authenticated student."""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        # Auto-create if admin testing or missing
        profile = StudentProfile(
            user_id=current_user.id,
            student_id=f"STU-{current_user.id:04d}",
            department="Computer Science",
            semester=4,
            academic_year="2025-2026"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

def get_current_teacher(
    current_user: User = Depends(require_role(["TEACHER", "ADMIN"])),
    db: Session = Depends(get_db)
) -> TeacherProfile:
    """Retrieve the TeacherProfile for the current authenticated teacher."""
    profile = db.query(TeacherProfile).filter(TeacherProfile.user_id == current_user.id).first()
    if not profile:
        profile = TeacherProfile(
            user_id=current_user.id,
            employee_id=f"TCH-{current_user.id:04d}",
            department="Computer Science & Engineering"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

require_admin = require_role(["ADMIN"])
