"""
Base Repository Pattern
Provides common CRUD operations for all repositories
"""

from datetime import datetime
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import desc
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository with common database operations"""

    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def create(self, **kwargs) -> T:
        """Create a new record"""
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get_by_id(self, id: str) -> Optional[T]:
        """Get record by ID"""
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        """Get all records with pagination"""
        return self.session.query(self.model).offset(offset).limit(limit).all()

    def update(self, id: str, **kwargs) -> Optional[T]:
        """Update a record"""
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            instance.updated_at = datetime.utcnow()
            self.session.commit()
            self.session.refresh(instance)
        return instance

    def delete(self, id: str) -> bool:
        """Delete a record"""
        instance = self.get_by_id(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False

    def count(self) -> int:
        """Count total records"""
        return self.session.query(self.model).count()
