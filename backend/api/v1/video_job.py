import uuid
import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.video_job import VideoJob
from backend.models.detection import Detection

router = APIRouter(
    prefix="/video-jobs",
    tags=["Video Jobs"],
)

@router.get("")
def get_all_jobs(db: Session = Depends(get_db)):
    """Mengambil semua riwayat video yang pernah diunggah."""
    return db.query(VideoJob).order_by(VideoJob.created_at.desc()).all()

@router.get("/{job_id}")
def get_job(job_id: uuid.UUID, db: Session = Depends(get_db)):
    """Mengambil status progres proses AI untuk satu video."""
    job = db.query(VideoJob).filter(VideoJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.delete("/{job_id}")
def delete_job(job_id: uuid.UUID, db: Session = Depends(get_db)):
    """Menghapus video beserta seluruh file fisik dan datanya dari SQLite."""
    job = db.query(VideoJob).filter(VideoJob.id == job_id).first()
    if job:
        # Ambil semua data deteksi yang terkait dengan video ini
        detections = db.query(Detection).filter(Detection.video_job_id == job_id).all()
        
        # 1. Hapus SEMUA file fisik foto (crops) dari hard disk agar tidak jadi sampah
        for det in detections:
            crop_file = Path(det.crop_path)
            if crop_file.exists():
                try:
                    crop_file.unlink()  # Perintah untuk mendelete file
                except Exception as e:
                    print(f"Gagal hapus file {crop_file}: {e}")

        # 2. Hapus data dari Database
        db.query(Detection).filter(Detection.video_job_id == job_id).delete(synchronize_session=False)
        db.delete(job)
        db.commit()
        
    return {"status": "success", "message": "Berhasil dihapus dari DB dan Hard disk!"}
