from ultralytics import YOLO


class ByteTracker:
    """
    Wrapper sederhana untuk fitur tracking YOLO11 + ByteTrack.
    """

    def __init__(self, model: YOLO):
        self.model = model

    def track(self, frame):
        """
        Menjalankan object tracking pada satu frame.
        """

        results = self.model.track(
            source=frame,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False,
        )

        return results