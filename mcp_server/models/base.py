"""
Base model class with common functionality.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TimestampMixin:
    """Mixin class to add timestamp fields to models."""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class BaseModel(Base, TimestampMixin):
    """Abstract base model with common functionality."""
    
    __abstract__ = True
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def validate(self):
        """Validate model data. Override in subclasses for custom validation."""
        pass
    
    def __repr__(self):
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', 'N/A')})>"