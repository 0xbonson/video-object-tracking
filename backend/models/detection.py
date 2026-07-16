import uuid
from typing import Any, Dict
from sqlalchemy import String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.base import BaseModel, TimestampMixin

class Detection(BaseModel, TimestampMixin):
    __tablename__ = "detections"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    
    # Foreign Key ke video_jobs.id dengan pengamanan ondelete="CASCADE"
    video_job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("video_jobs.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Track ID diindeks karena kita akan sering melakukan filter/pencarian ID yang sama
    track_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    frame_number: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    crop_path: Mapped[str] = mapped_column(String(512), nullable=False)
    
    # Kolom JSON untuk menampung output dinamis dari VLM (Vision Language Model)
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    # Relasi Many-to-One balik ke VideoJob
    video_job: Mapped["VideoJob"] = relationship(back_populates="detections")