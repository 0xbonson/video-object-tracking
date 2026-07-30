from backend.database.session import SessionLocal
from backend.models.video_job import VideoJob
from backend.models.detection import Detection

def clean_database():
    db = SessionLocal()
    
    # Daftar nama file palsu yang kita suntikkan tadi
    fake_filenames = [
        "lobby_cam_utama.mp4", 
        "basement_parking_B1.mp4", 
        "kantin_area_foodcourt.mp4"
    ]
    
    jobs = db.query(VideoJob).filter(VideoJob.filename.in_(fake_filenames)).all()
    
    deleted_jobs = 0
    for job in jobs:
        # Hapus deteksi yang terkait dengan job palsu ini
        db.query(Detection).filter(Detection.video_job_id == job.id).delete()
        # Hapus job-nya
        db.delete(job)
        deleted_jobs += 1
        
    db.commit()
    db.close()
    
    print(f"✅ Berhasil menghapus {deleted_jobs} data video palsu beserta deteksinya!")

if __name__ == "__main__":
    clean_database()
