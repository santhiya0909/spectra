from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint verifying API and Database status."""
    db_healthy = False
    try:
        db.execute(text("SELECT 1"))
        db_healthy = True
    except Exception as e:
        db_healthy = False

    return {
        "status": "healthy" if db_healthy else "degraded",
        "service": "SPECTRA Educational API",
        "database": "connected" if db_healthy else "unreachable",
        "version": "1.0.0"
    }
