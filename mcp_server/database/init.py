"""
Database initialization utilities.
"""

import logging
from typing import Optional

from .config import DatabaseConfig
from .connection import DatabaseManager, init_database
from ..migrations.manager import MigrationManager

logger = logging.getLogger(__name__)


def setup_database(config: Optional[DatabaseConfig] = None) -> DatabaseManager:
    """
    Set up database with configuration, connection, and initial schema.
    
    Args:
        config: Database configuration. If None, loads from environment.
        
    Returns:
        Initialized DatabaseManager instance.
    """
    try:
        # Initialize database manager
        db_manager = init_database(config)
        
        # Import the migration class dynamically to avoid import issues
        from ..migrations.versions.initial_schema import InitialSchemaMigration
        
        # Set up migration manager
        migration_manager = MigrationManager(db_manager)
        migration_manager.add_migration(InitialSchemaMigration())
        
        # Apply migrations
        migration_manager.migrate()
        
        logger.info("Database setup completed successfully")
        return db_manager
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise


def reset_database(config: Optional[DatabaseConfig] = None) -> DatabaseManager:
    """
    Reset database by dropping and recreating all tables.
    
    Args:
        config: Database configuration. If None, loads from environment.
        
    Returns:
        Initialized DatabaseManager instance.
    """
    try:
        # Initialize database manager
        db_manager = init_database(config)
        
        # Drop all tables
        db_manager.drop_tables()
        
        # Import the migration class dynamically
        from ..migrations.versions.initial_schema import InitialSchemaMigration
        
        # Set up migration manager and apply migrations
        migration_manager = MigrationManager(db_manager)
        migration_manager.add_migration(InitialSchemaMigration())
        migration_manager.migrate()
        
        logger.info("Database reset completed successfully")
        return db_manager
        
    except Exception as e:
        logger.error(f"Database reset failed: {e}")
        raise


def check_database_health(config: Optional[DatabaseConfig] = None) -> dict:
    """
    Check database connectivity and health.
    
    Args:
        config: Database configuration. If None, loads from environment.
        
    Returns:
        Dictionary with health check results.
    """
    try:
        db_manager = DatabaseManager(config or DatabaseConfig.from_env())
        return db_manager.health_check()
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }