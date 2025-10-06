"""
Database connection and session management.
"""

import logging
from contextlib import contextmanager
from typing import Generator, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.pool import QueuePool

from ..models.base import Base
from .config import DatabaseConfig

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """Initialize database manager with configuration."""
        self.config = config or DatabaseConfig.from_env()
        self.config.validate()
        
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
    
    @property
    def engine(self) -> Engine:
        """Get or create database engine."""
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine
    
    @property
    def session_factory(self) -> sessionmaker:
        """Get or create session factory."""
        if self._session_factory is None:
            self._session_factory = sessionmaker(bind=self.engine)
        return self._session_factory
    
    def _create_engine(self) -> Engine:
        """Create SQLAlchemy engine with connection pooling."""
        try:
            engine = create_engine(
                self.config.connection_string,
                poolclass=QueuePool,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                echo=self.config.echo,
                future=True
            )
            
            logger.info(f"Created database engine for {self.config.host}:{self.config.port}/{self.config.database}")
            return engine
            
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            raise
    
    def create_tables(self) -> None:
        """Create all database tables."""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def drop_tables(self) -> None:
        """Drop all database tables."""
        try:
            Base.metadata.drop_all(self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get database session with automatic cleanup."""
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def health_check(self) -> dict:
        """Check database connectivity and return status."""
        try:
            with self.get_session() as session:
                # Simple query to test connectivity
                result = session.execute(text("SELECT 1"))
                result.fetchone()
                
            return {
                "status": "healthy",
                "database": self.config.database,
                "host": self.config.host,
                "port": self.config.port
            }
            
        except OperationalError as e:
            logger.error(f"Database connection failed: {e}")
            return {
                "status": "unhealthy",
                "error": "Connection failed",
                "database": self.config.database,
                "host": self.config.host,
                "port": self.config.port
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "database": self.config.database,
                "host": self.config.host,
                "port": self.config.port
            }
    
    def close(self) -> None:
        """Close database connections."""
        if self._engine:
            self._engine.dispose()
            logger.info("Database connections closed")


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def init_database(config: Optional[DatabaseConfig] = None) -> DatabaseManager:
    """Initialize global database manager."""
    global _db_manager
    _db_manager = DatabaseManager(config)
    return _db_manager


def get_db_manager() -> DatabaseManager:
    """Get global database manager instance."""
    if _db_manager is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return _db_manager


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get database session from global manager."""
    db_manager = get_db_manager()
    with db_manager.get_session() as session:
        yield session