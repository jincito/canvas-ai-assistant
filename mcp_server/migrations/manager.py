"""
Migration management system.
"""

import logging
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Text, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.base import Base, BaseModel
from ..database.connection import DatabaseManager
from .base import Migration

logger = logging.getLogger(__name__)


class MigrationRecord(BaseModel):
    """Model to track applied migrations."""
    
    __tablename__ = 'migration_history'
    
    version = Column(String(50), primary_key=True)
    description = Column(String(255), nullable=False)
    applied_at = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f"<MigrationRecord(version={self.version}, applied_at={self.applied_at})>"


class MigrationManager:
    """Manages database migrations."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize migration manager."""
        self.db_manager = db_manager
        self.migrations: List[Migration] = []
    
    def add_migration(self, migration: Migration) -> None:
        """Add a migration to the manager."""
        self.migrations.append(migration)
        # Sort migrations by version
        self.migrations.sort(key=lambda m: m.version)
    
    def _ensure_migration_table(self, session: Session) -> None:
        """Ensure migration history table exists."""
        try:
            # Create migration history table if it doesn't exist
            MigrationRecord.__table__.create(self.db_manager.engine, checkfirst=True)
        except Exception as e:
            logger.error(f"Failed to create migration history table: {e}")
            raise
    
    def get_applied_migrations(self, session: Session) -> List[str]:
        """Get list of applied migration versions."""
        try:
            self._ensure_migration_table(session)
            records = session.query(MigrationRecord).all()
            return [record.version for record in records]
        except Exception as e:
            logger.error(f"Failed to get applied migrations: {e}")
            return []
    
    def apply_migration(self, migration: Migration, session: Session) -> None:
        """Apply a single migration."""
        try:
            logger.info(f"Applying migration {migration.version}: {migration.description}")
            
            # Apply the migration
            migration.up(session)
            
            # Record the migration
            record = MigrationRecord(
                version=migration.version,
                description=migration.description,
                applied_at=migration.timestamp
            )
            session.add(record)
            session.commit()
            
            logger.info(f"Successfully applied migration {migration.version}")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to apply migration {migration.version}: {e}")
            raise
    
    def rollback_migration(self, migration: Migration, session: Session) -> None:
        """Rollback a single migration."""
        try:
            logger.info(f"Rolling back migration {migration.version}: {migration.description}")
            
            # Rollback the migration
            migration.down(session)
            
            # Remove the migration record
            record = session.query(MigrationRecord).filter_by(version=migration.version).first()
            if record:
                session.delete(record)
            
            session.commit()
            
            logger.info(f"Successfully rolled back migration {migration.version}")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to rollback migration {migration.version}: {e}")
            raise
    
    def migrate(self) -> None:
        """Apply all pending migrations."""
        with self.db_manager.get_session() as session:
            applied_versions = self.get_applied_migrations(session)
            
            pending_migrations = [
                migration for migration in self.migrations
                if migration.version not in applied_versions
            ]
            
            if not pending_migrations:
                logger.info("No pending migrations")
                return
            
            logger.info(f"Applying {len(pending_migrations)} pending migrations")
            
            for migration in pending_migrations:
                self.apply_migration(migration, session)
            
            logger.info("All migrations applied successfully")
    
    def rollback(self, target_version: Optional[str] = None) -> None:
        """Rollback migrations to target version."""
        with self.db_manager.get_session() as session:
            applied_versions = self.get_applied_migrations(session)
            
            # Find migrations to rollback
            migrations_to_rollback = []
            for migration in reversed(self.migrations):
                if migration.version in applied_versions:
                    migrations_to_rollback.append(migration)
                    if target_version and migration.version == target_version:
                        break
            
            if not migrations_to_rollback:
                logger.info("No migrations to rollback")
                return
            
            logger.info(f"Rolling back {len(migrations_to_rollback)} migrations")
            
            for migration in migrations_to_rollback:
                self.rollback_migration(migration, session)
            
            logger.info("Rollback completed successfully")
    
    def status(self) -> dict:
        """Get migration status."""
        try:
            with self.db_manager.get_session() as session:
                applied_versions = self.get_applied_migrations(session)
                
                pending_migrations = [
                    migration for migration in self.migrations
                    if migration.version not in applied_versions
                ]
                
                return {
                    "total_migrations": len(self.migrations),
                    "applied_migrations": len(applied_versions),
                    "pending_migrations": len(pending_migrations),
                    "applied_versions": applied_versions,
                    "pending_versions": [m.version for m in pending_migrations]
                }
        except Exception as e:
            logger.error(f"Failed to get migration status: {e}")
            return {
                "error": str(e)
            }