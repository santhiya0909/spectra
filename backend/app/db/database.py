import os
import re
from urllib.parse import quote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

def normalize_database_url(url: str) -> str:
    """Normalize database URL for SQLAlchemy and safely encode special characters in password."""
    if not url:
        return url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    # If it's a PostgreSQL URL with an unencoded '@' in password, encode it
    try:
        pattern = r"^(postgresql(?:\+[a-z0-9]+)?://)([^:]+):(.*)@([^@/]+(?::\d+)?(?:/.*)?)$"
        match = re.match(pattern, url)
        if match:
            scheme, user, raw_pass, host_part = match.groups()
            if "@" in raw_pass and "%40" not in raw_pass:
                encoded_pass = quote(raw_pass, safe="")
                url = f"{scheme}{user}:{encoded_pass}@{host_part}"
    except Exception:
        pass

    return url

database_url = normalize_database_url(settings.DATABASE_URL)

connect_args = {}
if database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(
        database_url,
        connect_args=connect_args,
        pool_pre_ping=True
    )
    # Test connection
    with engine.connect() as conn:
        pass
except Exception as e:
    # If remote postgres fails or is not ready locally, fall back safely to sqlite
    print(f"[Warning] Failed connecting to {database_url}: {e}. Falling back to SQLite local database.")
    database_url = "sqlite:///./spectra.db"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency that provides an isolated SQLAlchemy database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Creates all database tables defined in SQLAlchemy models."""
    from app.db import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
