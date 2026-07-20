from uuid import UUID

from sqlalchemy.orm import Session

from backend.core.enums import JobStatus
from backend.models.video_job import VideoJob
from backend.repositories import video_job as repo_video_job
from backend.schemas.video_job import VideoJobCreate, VideoJobUpdate


class VideoJobService:
    """
    Service layer untuk mengelola business logic Video Job.
    """

    @staticmethod
    def create_job(
        db: Session,
        *,
        filename: str,
    ) -> VideoJob:
        """
        Membuat pekerjaan video baru dengan status awal PENDING.
        """
        obj_in = VideoJobCreate(filename=filename)

        return repo_video_job.create(
            db=db,
            obj_in=obj_in,
        )

    @staticmethod
    def get_job(
        db: Session,
        *,
        job_id: UUID,
    ) -> VideoJob | None:
        """
        Mengambil satu Video Job berdasarkan ID.
        """
        return repo_video_job.get(
            db=db,
            id=job_id,
        )

    @staticmethod
    def get_all_jobs(
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[VideoJob]:
        """
        Mengambil seluruh Video Job.
        """
        return repo_video_job.get_multi(
            db=db,
            skip=skip,
            limit=limit,
        )

    @staticmethod
    def get_jobs_by_status(
        db: Session,
        *,
        status: JobStatus,
    ) -> list[VideoJob]:
        """
        Mengambil seluruh Video Job berdasarkan status.
        """
        return repo_video_job.get_by_status(
            db=db,
            status=status,
        )

    @staticmethod
    def update_progress(
        db: Session,
        *,
        job_id: UUID,
        status: JobStatus,
        progress: int,
    ) -> VideoJob | None:
        """
        Memperbarui status dan progress Video Job.
        """
        db_obj = repo_video_job.get(
            db=db,
            id=job_id,
        )

        if db_obj is None:
            return None

        obj_in = VideoJobUpdate(
            status=status,
            progress=progress,
        )

        return repo_video_job.update(
            db=db,
            db_obj=db_obj,
            obj_in=obj_in,
        )


video_job_service = VideoJobService()