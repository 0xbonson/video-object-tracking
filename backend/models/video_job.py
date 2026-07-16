import uuid
from typing import List

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.enums import JobStatus
from backend.database.base import BaseModel, TimestampMixin


class VideoJob(BaseModel, TimestampMixin):
    """
    Model untuk merepresentasikan satu pekerjaan pemrosesan video.
    """

    __tablename__ = "video_jobs"

    # Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    # Nama file video yang diunggah
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Status proses video
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus),
        default=JobStatus.PENDING,
        nullable=False,
        index=True,
    )

    # Progress pemrosesan (0–100)
    progress: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # Relasi One-to-Many ke Detection
    detections: Mapped[List["Detection"]] = relationship(
        back_populates="video_job",
        cascade="all, delete-orphan",
    )