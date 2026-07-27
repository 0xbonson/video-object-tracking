from sqlalchemy.orm import Session

from backend.repositories.search import search_repository


class SearchService:
    """
    Service untuk pencarian detection berdasarkan
    atribut hasil Vision Language Model.
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
    ):
        return search_repository.search(
            db=db,
            shirt_color=shirt_color,
            shirt_type=shirt_type,
            pants_color=pants_color,
            pants_type=pants_type,
            gender=gender,
            object_name=object_name,
        )


search_service = SearchService()