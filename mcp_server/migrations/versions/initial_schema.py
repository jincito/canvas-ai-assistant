"""
Initial database schema migration.
Creates tables for courses, assignments, announcements, and grades.
"""

from sqlalchemy.orm import Session
from ..base import Migration
from ...models.base import Base


class InitialSchemaMigration(Migration):
    """Initial database schema setup."""
    
    def __init__(self):
        super().__init__(
            version="001",
            description="Create initial database schema for courses, assignments, announcements, and grades"
        )
    
    def up(self, session: Session) -> None:
        """Create all tables."""
        # Import models to ensure they're registered with Base
        from ...models import Course, Assignment, Announcement, Grade
        
        # Create all tables
        Base.metadata.create_all(session.bind)
    
    def down(self, session: Session) -> None:
        """Drop all tables."""
        # Import models to ensure they're registered with Base
        from ...models import Course, Assignment, Announcement, Grade
        
        # Drop all tables
        Base.metadata.drop_all(session.bind)