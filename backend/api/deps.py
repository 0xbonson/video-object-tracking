from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency untuk menyediakan database session pada setiap request.
    Session akan ditutup otomatis setelah request selesai.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
