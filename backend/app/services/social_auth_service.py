"""
Social OAuth service — verifies Google / Facebook tokens server-side,
then finds or creates a SPECTRA user and returns a JWT Token.

Credential setup
─────────────────
Google  → GOOGLE_CLIENT_ID  in backend/.env
Facebook → FACEBOOK_APP_ID + FACEBOOK_APP_SECRET  in backend/.env
"""

from __future__ import annotations

import secrets
import string
from typing import Optional

import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.models.user import User, StudentProfile, AuditLog
from app.db.models.academic import Subject, Enrollment
from app.schemas.auth import Token
from app.services.auth_service import create_user_token


# ── helpers ──────────────────────────────────────────────────────────────────

def _random_password(length: int = 32) -> str:
    """Generate a cryptographically random placeholder password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _find_or_create_social_user(
    db: Session,
    email: str,
    name: str,
    provider: str,
) -> User:
    """
    If a SPECTRA account already exists for this email, return it.
    Otherwise, create a new STUDENT account (social users are always
    provisioned as students — admins/teachers must use email/password).
    """
    email = email.lower().strip()
    user: Optional[User] = db.query(User).filter(User.email == email).first()

    if user:
        return user

    # ── Create new account ────────────────────────────────────────────────────
    placeholder_pw = _random_password()
    user = User(
        name=name.strip() or email.split("@")[0],
        email=email,
        password_hash=get_password_hash(placeholder_pw),
        role="STUDENT",
    )
    db.add(user)
    db.flush()

    # Student profile
    profile = StudentProfile(
        user_id=user.id,
        student_id=f"STU-{user.id:04d}",
        department="Computer Science",
        semester=4,
        academic_year="2025-2026",
    )
    db.add(profile)
    db.flush()

    # Default subject enrollments
    default_subject_codes = ["JAVA", "PYTHON", "DBMS", "STAT", "ECO"]
    subjects = (
        db.query(Subject)
        .filter(Subject.code.in_(default_subject_codes))
        .all()
    )
    for subject in subjects:
        exists = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id == profile.id,
                Enrollment.subject_id == subject.id,
            )
            .first()
        )
        if not exists:
            db.add(Enrollment(student_id=profile.id, subject_id=subject.id))

    # Audit log
    db.add(
        AuditLog(
            user_id=user.id,
            action=f"SOCIAL_REGISTER_{provider.upper()}",
            entity="USER",
            entity_id=str(user.id),
        )
    )

    db.commit()
    db.refresh(user)
    return user


# ── Google ────────────────────────────────────────────────────────────────────

async def verify_google_token(id_token: str) -> dict:
    """
    Verify a Google ID token by calling Google's tokeninfo endpoint.
    Returns the payload dict on success, raises HTTPException on failure.
    """
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google Sign-In is not configured on this server.",
        )

    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token. Please try again.",
        )

    payload = resp.json()

    # Audience check — the token must be issued for OUR client ID
    aud = payload.get("aud", "")
    if aud != settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google token audience mismatch.",
        )

    if not payload.get("email_verified") or payload.get("email_verified") == "false":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account email is not verified.",
        )

    return payload


async def google_social_login(id_token: str, db: Session) -> Token:
    payload = await verify_google_token(id_token)
    email = payload.get("email", "")
    name = payload.get("name", "") or payload.get("given_name", "")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google did not return an email address.",
        )

    user = _find_or_create_social_user(db, email, name, "GOOGLE")

    # Audit login
    db.add(
        AuditLog(
            user_id=user.id,
            action="SOCIAL_LOGIN_GOOGLE",
            entity="USER",
            entity_id=str(user.id),
        )
    )
    db.commit()

    return create_user_token(user)


# ── Facebook ──────────────────────────────────────────────────────────────────

async def verify_facebook_token(access_token: str) -> dict:
    """
    Verify a Facebook user access token via the Graph API's /me endpoint.
    We also call /debug_token with the app token to validate the audience.
    """
    if not settings.FACEBOOK_APP_ID or not settings.FACEBOOK_APP_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Facebook Login is not configured on this server.",
        )

    app_token = f"{settings.FACEBOOK_APP_ID}|{settings.FACEBOOK_APP_SECRET}"

    async with httpx.AsyncClient(timeout=10) as client:
        # 1️⃣ Debug / validate the token
        debug_resp = await client.get(
            "https://graph.facebook.com/debug_token",
            params={
                "input_token": access_token,
                "access_token": app_token,
            },
        )
        if debug_resp.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Facebook token. Please try again.",
            )

        debug_data = debug_resp.json().get("data", {})
        if not debug_data.get("is_valid"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Facebook token is no longer valid.",
            )
        if str(debug_data.get("app_id")) != str(settings.FACEBOOK_APP_ID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Facebook token was not issued for this application.",
            )

        # 2️⃣ Fetch user profile
        me_resp = await client.get(
            "https://graph.facebook.com/me",
            params={
                "access_token": access_token,
                "fields": "id,name,email",
            },
        )

    if me_resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not retrieve Facebook profile.",
        )

    return me_resp.json()


async def facebook_social_login(access_token: str, db: Session) -> Token:
    payload = await verify_facebook_token(access_token)
    email = payload.get("email", "")
    name = payload.get("name", "")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Facebook did not return an email address. "
                "Please make sure your Facebook account has a verified email "
                "and that you granted email permissions."
            ),
        )

    user = _find_or_create_social_user(db, email, name, "FACEBOOK")

    db.add(
        AuditLog(
            user_id=user.id,
            action="SOCIAL_LOGIN_FACEBOOK",
            entity="USER",
            entity_id=str(user.id),
        )
    )
    db.commit()

    return create_user_token(user)
