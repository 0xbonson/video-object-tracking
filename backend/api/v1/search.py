from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.services.search import search_service

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get("")
def search(
    shirt_color: str | None = Query(default=None),
    shirt_type: str | None = Query(default=None),
    pants_color: str | None = Query(default=None),
    pants_type: str | None = Query(default=None),
    gender: str | None = Query(default=None),
    object_name: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return search_service.search(
        db=db,
        shirt_color=shirt_color,
        shirt_type=shirt_type,
        pants_color=pants_color,
        pants_type=pants_type,
        gender=gender,
        object_name=object_name,
    )