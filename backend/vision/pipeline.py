from pathlib import Path

import cv2

from backend.vision.detector import detector
from backend.vision.tracker import ByteTracker
from backend.vision.vlm import vlm

CROP_DIR = Path("backend/storage/crops")
CROP_DIR.mkdir(parents=True, exist_ok=True)


class VideoPipeline:
    """
    Video -> YOLO -> ByteTrack -> Crop -> VLM

    VLM hanya dipanggil SATU KALI untuk setiap track_id.
    Hasilnya di-cache sehingga frame berikutnya tidak
    mengirim request lagi ke Ollama.
    """

    def __init__(self):
        self.tracker = ByteTracker(detector.model)

    def process(self, video_path: str | Path):
        video_path = str(video_path)

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise RuntimeError(
                f"Gagal membuka video: {video_path}"
            )

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30.0

        frame_number = 0
        detections = []

        # Cache hasil VLM berdasarkan track_id
        processed_tracks: dict[int, dict] = {}

        while True:
            success, frame = cap.read()

            if not success:
                break

            frame_number += 1

            results = self.tracker.track(frame)

            if not results:
                continue

            result = results[0]

            if result.boxes is None:
                continue

            for box in result.boxes:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist(),
                )

                track_id = -1
                if box.id is not None:
                    track_id = int(box.id[0])

                crop = frame[y1:y2, x1:x2]

                if crop.size == 0:
                    continue

                filename = (
                    f"frame_{frame_number:06d}"
                    f"_track_{track_id}.jpg"
                )

                crop_path = CROP_DIR / filename

                cv2.imwrite(
                    str(crop_path),
                    crop,
                )

                # Jalankan VLM hanya sekali untuk setiap track
                if track_id not in processed_tracks:

                    try:
                        print(
                            f"[VLM] Analysing track {track_id}..."
                        )

                        attributes = vlm.describe(
                            crop_path
                        )

                    except Exception as exc:
                        print(
                            f"VLM ERROR ({crop_path}): {exc}"
                        )

                        class_id = int(box.cls[0])

                        attributes = {
                            "object": detector.model.names[class_id],
                            "confidence": float(box.conf[0]),
                        }

                    processed_tracks[track_id] = attributes

                attributes = processed_tracks[track_id]

                detections.append(
                    {
                        "track_id": track_id,
                        "frame_number": frame_number,
                        "timestamp_seconds": (
                            frame_number / fps
                        ),
                        "crop_path": str(crop_path),
                        "attributes": attributes,
                    }
                )

        cap.release()

        return detections