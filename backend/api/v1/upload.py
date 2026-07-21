import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.api.deps import get_db
from backend.schemas.video_job import VideoJobRead
from backend.services import video_job_service

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

# Folder penyimpanan video
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
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> VideoJobRead:
    """
    Upload video ke server lalu membuat VideoJob baru.
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

    return job