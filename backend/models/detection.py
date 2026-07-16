from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from backend.models.video_job import VideoJob


class Detection(BaseModel, TimestampMixin):
    """
    Model untuk menyimpan hasil deteksi objek pada setiap frame video.
    """

    __tablename__ = "detections"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign Key ke VideoJob
    video_job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("video_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Track ID dari ByteTrack
    track_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    frame_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    timestamp_seconds: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    crop_path: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    # Output Vision Language Model
    attributes: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
    )

    # Relasi Many-to-One ke VideoJob
    video_job: Mapped[VideoJob] = relationship(
        back_populates="detections",
    )