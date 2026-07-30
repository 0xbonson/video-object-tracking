from pathlib import Path
import cv2

from backend.vision.detector import detector
from backend.vision.tracker import ByteTracker
from backend.vision.vlm import vlm

CROP_DIR = Path("backend/storage/crops")
CROP_DIR.mkdir(parents=True, exist_ok=True)


class VideoPipeline:
    """
    Video -> YOLO -> ByteTrack -> Filter Person & Size -> Time-Based Crop -> VLM
    """

    def __init__(self):
        self.tracker = ByteTracker(detector.model)

    def process(self, video_path: str | Path):
        video_path = str(video_path)
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise RuntimeError(f"Gagal membuka video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30.0

        # Ambil resolusi video untuk menghitung luas layar
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_area = frame_width * frame_height

        frame_number = 0
        detections = []
        last_analyzed_time: dict[int, float] = {}

        while True:
            success, frame = cap.read()
            if not success:
                break

            frame_number += 1
            current_time_sec = frame_number / fps

            results = self.tracker.track(frame)
            if not results:
                continue

            result = results[0]
            if result.boxes is None:
                continue

            for box in result.boxes:
                class_id = int(box.cls[0])
                yolo_object = detector.model.names[class_id]
                
                # 1. Pastikan itu adalah manusia
                if yolo_object != "person":
                    continue
                
                # 2. Pastikan ByteTrack SUDAH memberikan ID! (Mencegah error Pydantic -1)
                if box.id is None:
                    continue
                
                track_id = int(box.id[0])

                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                
                # 3. FILTER UKURAN (Area Thresholding)
                # Hitung luas kotak orang ini
                box_area = (x2 - x1) * (y2 - y1)
                
                # Jika ukuran orang ini kurang dari 15% total layar, abaikan! (Penari latar/Penonton)
                if box_area < (frame_area * 0.15):
                    continue

                # 4. Time-Based Sampling (3 detik)
                last_time = last_analyzed_time.get(track_id, -999.0)
                if (current_time_sec - last_time) < 3.0:
                    continue 

                crop = frame[y1:y2, x1:x2]
                if crop.size == 0:
                    continue

                filename = f"frame_{frame_number:06d}_track_{track_id}.jpg"
                crop_path = CROP_DIR / filename
                cv2.imwrite(str(crop_path), crop)

                try:
                    print(f"[VLM] Menganalisis Bintang Utama (Track {track_id}) pada detik {current_time_sec:.1f}...")
                    vlm_attributes = vlm.describe(crop_path)
                    
                    attributes = {
                        "object": "person",
                        **vlm_attributes,
                    }

                except Exception as exc:
                    print(f"VLM ERROR ({crop_path}): {exc}")
                    attributes = {
                        "object": "person",
                        "confidence": float(box.conf[0]),
                    }

                last_analyzed_time[track_id] = current_time_sec

                detections.append(
                    {
                        "track_id": track_id,
                        "frame_number": frame_number,
                        "timestamp_seconds": current_time_sec,
                        "crop_path": str(crop_path),
                        "attributes": attributes,
                    }
                )

        cap.release()
        return detections
