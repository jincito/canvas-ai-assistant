"""
Base migration class and utilities.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy.orm import Session


class Migration(ABC):
    """Base class for database migrations."""
    
    def __init__(self, version: str, description: str):
        """Initialize migration with version and description."""
        self.version = version
        self.description = description
        self.timestamp = datetime.utcnow()
    
    @abstractmethod
    def up(self, session: Session) -> None:
        """Apply the migration."""
        pass
    
    @abstractmethod
    def down(self, session: Session) -> None:
        """Rollback the migration."""
        pass
    
    def __str__(self) -> str:
        return f"Migration {self.version}: {self.description}"
    
    def __repr__(self) -> str:
        return f"<Migration(version={self.version}, description={self.description})>"