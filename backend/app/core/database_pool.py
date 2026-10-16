import asyncpg
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class DatabasePool:
    def __init__(self):
        self.pool = None
        
    async def initialize(self):
        """Initialize database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                settings.database_url,
                min_size=1,
                max_size=20,
            )
            logger.info("✅ Database connection pool initialized")
        except Exception as e:
            logger.error(f"❌ Database pool initialization failed: {e}")
            self.pool = None
    
    async def close(self):
        """Close database connections"""
        if self.pool:
            await self.pool.close()
    
    def get_connection(self):
        """Get a connection from the pool"""
        if not self.pool:
            raise Exception("Database pool not initialized")
        return self.pool.acquire()

# Global database pool instance
db_pool = DatabasePool()