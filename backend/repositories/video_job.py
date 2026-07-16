from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.enums import JobStatus
from backend.models.video_job import VideoJob
from backend.repositories.base import CRUDBase
from backend.schemas.video_job import VideoJobCreate, VideoJobUpdate


class CRUDVideoJob(
    CRUDBase[
        VideoJob,
        VideoJobCreate,
        VideoJobUpdate,
    ]
):
    def get_by_status(
        self,
        db: Session,
        status: JobStatus,
    ) -> list[VideoJob]:
        stmt = select(VideoJob).where(VideoJob.status == status)

        return list(db.execute(stmt).scalars().all())


video_job = CRUDVideoJob(VideoJob)