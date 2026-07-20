from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.deps import get_db
from backend.schemas.video_job import (
    VideoJobCreate,
    VideoJobRead,
    VideoJobUpdate,
)
from backend.services import video_job_service

router = APIRouter(
    prefix="/video-jobs",
    tags=["Video Jobs"],
)


@router.post(
    "",
    response_model=VideoJobRead,
    status_code=status.HTTP_201_CREATED,
)
def create_video_job(
    payload: VideoJobCreate,
    db: Session = Depends(get_db),
):
    return video_job_service.create_job(
        db=db,
        filename=payload.filename,
    )


@router.get(
    "",
    response_model=list[VideoJobRead],
)
def list_video_jobs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return video_job_service.get_all_jobs(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{job_id}",
    response_model=VideoJobRead,
)
def get_video_job(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    job = video_job_service.get_job(
        db=db,
        job_id=job_id,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video job not found.",
        )

    return job


@router.patch(
    "/{job_id}",
    response_model=VideoJobRead,
)
def update_video_job(
    job_id: UUID,
    payload: VideoJobUpdate,
    db: Session = Depends(get_db),
):
    job = video_job_service.update_progress(
        db=db,
        job_id=job_id,
        status=payload.status,
        progress=payload.progress,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video job not found.",
        )

    return job