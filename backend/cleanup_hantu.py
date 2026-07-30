from pathlib import Path
from backend.database.session import SessionLocal
from backend.models.video_job import VideoJob
from backend.models.detection import Detection

def bersihkan_sistem():
    db = SessionLocal()
    try:
        # 1. Hapus semua data hantu di database
        db.query(Detection).delete()
        db.query(VideoJob).delete()
        db.commit()
        print("✅ Database berhasil dibersihkan dari data yatim piatu!")
    except Exception as e:
        print(f"❌ Gagal membersihkan database: {e}")
    finally:
        db.close()

    # 2. Sapu bersih semua file fisik yang tersisa
    crop_dir = Path("backend/storage/crops")
    if crop_dir.exists():
        count = 0
        for f in crop_dir.glob("*.jpg"):
            f.unlink()
            count += 1
        print(f"✅ Berhasil menghapus {count} file foto hantu dari hard disk!")

if __name__ == "__main__":
    bersihkan_sistem()
