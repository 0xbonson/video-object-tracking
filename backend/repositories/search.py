from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.detection import Detection


class SearchRepository:
    """
    Repository untuk pencarian Detection
    berdasarkan attribute hasil VLM.
    """

    def search(
        self,
        db: Session,
        shirt_color: str | None = None,
        shirt_type: str | None = None,
        pants_color: str | None = None,
        pants_type: str | None = None,
        gender: str | None = None,
        object_name: str | None = None,
    ) -> list[Detection]:

        stmt = select(Detection)

        if shirt_color:
            stmt = stmt.where(
                Detection.attributes["shirt_color"].as_string()
                == shirt_color
            )

        if shirt_type:
            stmt = stmt.where(
                Detection.attributes["shirt_type"].as_string()
                == shirt_type
            )

        if pants_color:
            stmt = stmt.where(
                Detection.attributes["pants_color"].as_string()
                == pants_color
            )

        if pants_type:
            stmt = stmt.where(
                Detection.attributes["pants_type"].as_string()
                == pants_type
            )

        if gender:
            stmt = stmt.where(
                Detection.attributes["gender"].as_string()
                == gender
            )

        if object_name:
            stmt = stmt.where(
                Detection.attributes["object"].as_string()
                == object_name
            )

        stmt = stmt.order_by(Detection.frame_number)

        return list(db.execute(stmt).scalars().all())


search_repository = SearchRepository()