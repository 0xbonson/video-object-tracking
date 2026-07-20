from typing import Any

from sqlalchemy.orm import Session

from backend.models.detection import Detection
from backend.repositories import detection as repo_detection
from backend.schemas.detection import DetectionCreate


class DetectionService:
    """
    Service layer untuk mengelola business logic Detection.
    """

    @staticmethod
    def process_new_detection(
        db: Session,
        *,
        video_job_id,
        track_id: int,
        frame_number: int,
        timestamp_seconds: float,
        crop_path: str,
        attributes: dict[str, Any],
    ) -> Detection:
        """
        Business Rule:
        - Jika track_id yang sama muncul kembali
        - Dan atributnya sama
        - Dengan selisih waktu kurang dari 30 detik
        Maka UPDATE record terakhir, bukan INSERT baru.
        """

        last_detection = repo_detection.get_latest_by_track_id(
            db=db,
            video_job_id=video_job_id,
            track_id=track_id,
        )

        if last_detection is not None:
            time_diff = (
                timestamp_seconds
                - last_detection.timestamp_seconds
            )

            same_attributes = (
                last_detection.attributes == attributes
            )

            if same_attributes and time_diff < 30.0:
                update_data = {
                    "frame_number": frame_number,
                    "timestamp_seconds": timestamp_seconds,
                    "crop_path": crop_path,
                }

                return repo_detection.update(
                    db=db,
                    db_obj=last_detection,
                    obj_in=update_data,
                )

        obj_in = DetectionCreate(
            video_job_id=video_job_id,
            track_id=track_id,
            frame_number=frame_number,
            timestamp_seconds=timestamp_seconds,
            crop_path=crop_path,
            attributes=attributes,
        )

        return repo_detection.create(
            db=db,
            obj_in=obj_in,
        )

    @staticmethod
    def get_detections_for_video(
        db: Session,
        *,
        video_job_id,
    ) -> list[Detection]:
        """
        Mengambil seluruh Detection untuk satu Video Job.
        """
        return repo_detection.get_all_by_video(
            db=db,
            video_job_id=video_job_id,
        )


detection_service = DetectionService()