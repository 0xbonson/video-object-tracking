import uuid
import random
from datetime import datetime, timedelta, timezone

from backend.database.session import SessionLocal
from backend.models.video_job import VideoJob
from backend.models.detection import Detection

def seed_database():
    db = SessionLocal()
    
    # Referensi gambar yang sudah kita ketahui ada di sistem Anda
    existing_crops = [
        "backend/storage/crops/frame_000011_track_1.jpg",
        "backend/storage/crops/frame_000011_track_2.jpg",
    ]
    
    now = datetime.now(timezone.utc)
    
    # Skenario 1: Kamera Lobby (3 hari yang lalu)
    job1_id = uuid.uuid4()
    job1 = VideoJob(
        id=job1_id,
        filename="lobby_cam_utama.mp4",
        status="COMPLETED",
        progress=100,
        created_at=now - timedelta(days=3),
        updated_at=now - timedelta(days=3)
    )
    
    # Skenario 2: Kamera Basement (Kemarin)
    job2_id = uuid.uuid4()
    job2 = VideoJob(
        id=job2_id,
        filename="basement_parking_B1.mp4",
        status="COMPLETED",
        progress=100,
        created_at=now - timedelta(days=1),
        updated_at=now - timedelta(days=1)
    )
    
    # Skenario 3: Kamera Kantin (Hari ini)
    job3_id = uuid.uuid4()
    job3 = VideoJob(
        id=job3_id,
        filename="kantin_area_foodcourt.mp4",
        status="COMPLETED",
        progress=100,
        created_at=now - timedelta(hours=2),
        updated_at=now - timedelta(hours=2)
    )
    
    db.add_all([job1, job2, job3])
    
    # Deteksi fiktif untuk Job 1 (Lobby)
    det1 = Detection(
        video_job_id=job1_id, track_id=15, frame_number=300, timestamp_seconds=10.5,
        crop_path=existing_crops[0],
        attributes={"object": "person", "shirt_color": "red", "pants_color": "blue", "gender": "female"},
        created_at=job1.created_at
    )
    det2 = Detection(
        video_job_id=job1_id, track_id=16, frame_number=350, timestamp_seconds=12.0,
        crop_path=existing_crops[1],
        attributes={"object": "person", "shirt_color": "black", "pants_color": "black", "gender": "male"},
        created_at=job1.created_at
    )
    
    # Deteksi fiktif untuk Job 2 (Basement)
    det3 = Detection(
        video_job_id=job2_id, track_id=42, frame_number=1200, timestamp_seconds=40.0,
        crop_path=existing_crops[0],
        attributes={"object": "person", "shirt_color": "green", "pants_color": "jeans", "gender": "male"},
        created_at=job2.created_at
    )
    det4 = Detection(
        video_job_id=job2_id, track_id=43, frame_number=1250, timestamp_seconds=41.6,
        crop_path=existing_crops[1],
        attributes={"object": "person", "shirt_color": "red", "pants_color": "black", "gender": "male"},
        created_at=job2.created_at
    )
    
    # Deteksi fiktif untuk Job 3 (Kantin)
    det5 = Detection(
        video_job_id=job3_id, track_id=8, frame_number=210, timestamp_seconds=7.0,
        crop_path=existing_crops[0],
        attributes={"object": "person", "shirt_color": "white", "pants_color": "khaki", "gender": "female"},
        created_at=job3.created_at
    )
    
    db.add_all([det1, det2, det3, det4, det5])
    db.commit()
    db.close()
    
    print("✅ Mock data berhasil disuntikkan ke dalam database!")

if __name__ == "__main__":
    seed_database()
