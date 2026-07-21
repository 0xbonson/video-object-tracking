from pathlib import Path
from uuid import UUID


class VideoProcessor:
    """
    Worker yang bertugas memproses satu video.
    """

    def process(
        self,
        *,
        job_id: UUID,
        video_path: str | Path,
    ):
        raise NotImplementedError


video_processor = VideoProcessor()