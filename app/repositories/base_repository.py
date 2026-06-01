"""Base repository for CRUD operations."""

from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository for CRUD operations.

    Provides generic CRUD operations for database models.
    """

    def __init__(self, model: type[ModelType]):
        """
        Initialize repository.

        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    async def get(self, db: AsyncSession, record_id: int) -> ModelType | None:
        """
        Get record by ID.

        Args:
            db: Database session
            record_id: Record ID

        Returns:
            Optional[ModelType]: Record if found
        """
        result = await db.execute(select(self.model).where(getattr(self.model, "id") == record_id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """
        Get multiple records with pagination.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records

        Returns:
            List[ModelType]: List of records
        """
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """
        Create new record.

        Args:
            db: Database session
            obj_in: Pydantic schema with creation data

        Returns:
            ModelType: Created record
        """
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """
        Update record.

        Args:
            db: Database session
            db_obj: Existing database object
            obj_in: Pydantic schema with update data

        Returns:
            ModelType: Updated record
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, record_id: int) -> bool:
        """
        Delete record.

        Args:
            db: Database session
            record_id: Record ID

        Returns:
            bool: True if deleted
        """
        obj = await self.get(db, record_id)
        if obj:
            await db.delete(obj)
            return True
        return False
