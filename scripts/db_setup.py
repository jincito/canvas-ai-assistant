#!/usr/bin/env python3
"""
Database setup and management script for Canvas AI Assistant.
"""

import sys
import os
import logging
from pathlib import Path

# Add the parent directory to the path so we can import mcp_server
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server.database.init import setup_database, reset_database, check_database_health
from mcp_server.database.config import DatabaseConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main CLI function."""
    if len(sys.argv) < 2:
        print("Usage: python db_setup.py <command>")
        print("Commands:")
        print("  setup    - Initialize database and apply migrations")
        print("  reset    - Drop all tables and recreate schema")
        print("  health   - Check database connectivity")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == "setup":
            logger.info("Setting up database...")
            db_manager = setup_database()
            logger.info("Database setup completed successfully")
            
        elif command == "reset":
            logger.info("Resetting database...")
            db_manager = reset_database()
            logger.info("Database reset completed successfully")
            
        elif command == "health":
            logger.info("Checking database health...")
            health = check_database_health()
            print(f"Database status: {health['status']}")
            if health['status'] == 'healthy':
                print(f"Connected to: {health['host']}:{health['port']}/{health['database']}")
            else:
                print(f"Error: {health.get('error', 'Unknown error')}")
            
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Command failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()