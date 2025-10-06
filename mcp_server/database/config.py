"""
Database configuration management.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    
    host: str = "localhost"
    port: int = 5432
    database: str = "canvas_ai_assistant"
    username: str = "postgres"
    password: str = ""
    
    # Connection pool settings
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    
    # Connection settings
    echo: bool = False  # Set to True for SQL query logging
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create configuration from environment variables."""
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', 'canvas_ai_assistant'),
            username=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            pool_size=int(os.getenv('DB_POOL_SIZE', '5')),
            max_overflow=int(os.getenv('DB_MAX_OVERFLOW', '10')),
            pool_timeout=int(os.getenv('DB_POOL_TIMEOUT', '30')),
            pool_recycle=int(os.getenv('DB_POOL_RECYCLE', '3600')),
            echo=os.getenv('DB_ECHO', 'false').lower() == 'true'
        )
    
    @property
    def connection_string(self) -> str:
        """Generate PostgreSQL connection string."""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.host:
            raise ValueError("Database host is required")
        
        if not self.database:
            raise ValueError("Database name is required")
        
        if not self.username:
            raise ValueError("Database username is required")
        
        if self.port <= 0 or self.port > 65535:
            raise ValueError("Database port must be between 1 and 65535")
        
        if self.pool_size <= 0:
            raise ValueError("Pool size must be greater than 0")
        
        if self.max_overflow < 0:
            raise ValueError("Max overflow cannot be negative")