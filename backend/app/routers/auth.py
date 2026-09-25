from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import UserLogin, UserRegister, Token, UserOut
from app.services.auth_service import authenticate_user, register_user, create_user_token
from app.core.dependencies import get_current_user
from app.db.models.user import User, AuditLog

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Register a new student, teacher, or admin account."""
    user = register_user(db, user_in)
    return create_user_token(user)

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate with email and password, returning JWT bearer token."""
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Log login in audit
    audit = AuditLog(user_id=user.id, action="USER_LOGIN", entity="USER", entity_id=str(user.id))
    db.add(audit)
    db.commit()

    return create_user_token(user)

@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Get profile information for the authenticated user."""
    return current_user

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Acknowledge user logout."""
    return {"message": "Logged out successfully"}
