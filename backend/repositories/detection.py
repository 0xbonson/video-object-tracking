from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.detection import Detection
from backend.repositories.base import CRUDBase
from backend.schemas.detection import DetectionCreate, DetectionUpdate


class CRUDDetection(
    CRUDBase[
        Detection,
        DetectionCreate,
        DetectionUpdate,
    ]
):
    def get_latest_by_track_id(
        self,
        db: Session,
        *,
        video_job_id: UUID,
        track_id: int,
    ) -> Detection | None:
        stmt = (
            select(Detection)
            .where(
                Detection.video_job_id == video_job_id,
                Detection.track_id == track_id,
            )
            .order_by(Detection.frame_number.desc())
        )

        return db.execute(stmt).scalar_one_or_none()

    def get_all_by_video(
        self,
        db: Session,
        *,
        video_job_id: UUID,
    ) -> list[Detection]:
        stmt = select(Detection).where(
            Detection.video_job_id == video_job_id
        )

        return list(db.execute(stmt).scalars().all())


detection = CRUDDetection(Detection)