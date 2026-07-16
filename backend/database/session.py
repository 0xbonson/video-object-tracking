from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings

# SQLite memerlukan check_same_thread=False.
# Jika nanti pindah ke PostgreSQL, parameter ini tidak akan dipakai.
connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.is_development,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Dependency FastAPI untuk mendapatkan database session.
    Session akan otomatis ditutup setelah request selesai.
    """
    db = SessionLocal()
    try:
        yield db  
    finally:
        db.close()
