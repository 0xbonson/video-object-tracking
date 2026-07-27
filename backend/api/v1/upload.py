import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from backend.api.deps import get_db
from backend.schemas.video_job import VideoJobRead
from backend.services import video_job_service
from backend.workers.video_processor import video_processor

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

VIDEO_STORAGE = Path("backend/storage/videos")
VIDEO_STORAGE.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
}


@router.post(
    "",
    response_model=VideoJobRead,
    status_code=status.HTTP_201_CREATED,
)
def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> VideoJobRead:
    """
    Upload video kemudian langsung memulai proses object tracking
    di background.
    """

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported video format.",
        )

    filename = f"{uuid4()}{extension}"

    destination = VIDEO_STORAGE / filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job = video_job_service.create_job(
        db=db,
        filename=filename,
    )

    background_tasks.add_task(
        video_processor.process,
        job_id=job.id,
        video_path=destination,
    )

    return job