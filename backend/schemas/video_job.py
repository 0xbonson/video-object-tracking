from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from backend.core.enums import JobStatus


class VideoJobBase(BaseModel):
    filename: str = Field(..., min_length=1, max_length=255)
    status: JobStatus = JobStatus.PENDING
    progress: int = Field(default=0, ge=0, le=100)


class VideoJobCreate(VideoJobBase):
    pass


class VideoJobUpdate(BaseModel):
    status: JobStatus | None = None
    progress: int | None = Field(default=None, ge=0, le=100)


class VideoJobRead(VideoJobBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)