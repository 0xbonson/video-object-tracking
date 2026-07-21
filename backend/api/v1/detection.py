from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.deps import get_db
from backend.schemas.detection import DetectionRead
from backend.services import detection_service

router = APIRouter(
    prefix="/detections",
    tags=["Detections"],
)


@router.get(
    "/video/{video_job_id}",
    response_model=list[DetectionRead],
)
def get_detections_by_video(
    video_job_id: UUID,
    db: Session = Depends(get_db),
) -> list[DetectionRead]:
    """
    Mengambil seluruh hasil deteksi
    berdasarkan Video Job tertentu.
    """
    return detection_service.get_detections_for_video(
        db=db,
        video_job_id=video_job_id,
    )