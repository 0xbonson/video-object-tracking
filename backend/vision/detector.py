from ultralytics import YOLO


class YOLODetector:
    """
    Wrapper sederhana untuk model YOLO.
    Model hanya dimuat sekali saat object dibuat.
    """

    def __init__(
        self,
        model_path: str = "yolo11n.pt",
    ) -> None:
        self.model = YOLO(model_path)

    def predict(
        self,
        image,
        *,
        conf: float = 0.25,
        verbose: bool = False,
    ):
        """
        Menjalankan inferensi pada sebuah gambar (numpy array).

        Returns:
            list[Results]
        """
        return self.model.predict(
            source=image,
            conf=conf,
            verbose=verbose,
        )


detector = YOLODetector()
