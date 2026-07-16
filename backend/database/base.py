import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """
    Class fondasi deklaratif untuk SQLAlchemy 2.x.
    Semua model ORM sistem harus dan wajib mewarisi class ini.
    """
    pass

class TimestampMixin:
    """
    Mixin otomatis untuk menambahkan jejak waktu (audit trail) 
    ke setiap model database tanpa duplikasi kode.
    Menggunakan UTC timezone agar siap untuk PostgreSQL.
    """
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
