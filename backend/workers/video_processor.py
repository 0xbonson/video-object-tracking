from pathlib import Path
from uuid import UUID

from backend.core.enums import JobStatus
from backend.database.session import SessionLocal
from backend.services.detection import detection_service
from backend.services.video_job import video_job_service
from backend.vision.pipeline import VideoPipeline


class VideoProcessor:
    """
    Worker yang bertugas memproses satu video.

    Flow:
    1. Job -> RUNNING
    2. Jalankan VideoPipeline
    3. Simpan seluruh detection ke database
    4. Job -> COMPLETED

    Jika terjadi error:
    Job -> FAILED
    """

    def __init__(self):
        self.pipeline = VideoPipeline()

    def process(
        self,
        *,
        job_id: UUID,
        video_path: str | Path,
    ) -> None:
        db = SessionLocal()

        try:
            video_job_service.update_progress(
                db=db,
                job_id=job_id,
                status=JobStatus.RUNNING,
                progress=0,
            )

            detections = self.pipeline.process(video_path)

            total = len(detections)

            for index, detection in enumerate(detections, start=1):

                detection_service.process_new_detection(
                    db=db,
                    video_job_id=job_id,
                    track_id=detection["track_id"],
                    frame_number=detection["frame_number"],
                    timestamp_seconds=detection["timestamp_seconds"],
                    crop_path=detection["crop_path"],
                    attributes=detection["attributes"],
                )

                progress = int(index * 100 / total)

                video_job_service.update_progress(
                    db=db,
                    job_id=job_id,
                    status=JobStatus.RUNNING,
                    progress=progress,
                )

            video_job_service.update_progress(
                db=db,
                job_id=job_id,
                status=JobStatus.COMPLETED,
                progress=100,
            )

        except Exception:
            video_job_service.update_progress(
                db=db,
                job_id=job_id,
                status=JobStatus.FAILED,
                progress=0,
            )
            raise

        finally:
            db.close()


video_processor = VideoProcessor()