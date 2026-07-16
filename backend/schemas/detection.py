from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DetectionBase(BaseModel):
    video_job_id: UUID
    track_id: int = Field(..., ge=0)
    frame_number: int = Field(..., ge=0)
    timestamp_seconds: float = Field(..., ge=0)
    crop_path: str = Field(..., min_length=1)

    attributes: dict[str, Any] = Field(default_factory=dict)


class DetectionCreate(DetectionBase):
    pass


class DetectionUpdate(BaseModel):
    crop_path: str | None = None
    attributes: dict[str, Any] | None = None


class DetectionRead(DetectionBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)