from __future__ import annotations

from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel as PydanticModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD repository.
    """

    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, id: UUID) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == id)
        return db.execute(stmt).scalar_one_or_none()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def create(
        self,
        db: Session,
        *,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(
        self,
        db: Session,
        *,
        id: UUID,
    ) -> ModelType | None:
        obj = self.get(db, id)

        if obj is None:
            return None

        db.delete(obj)
        db.commit()

        return obj