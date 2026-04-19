"""Event store operations for gateway service."""
import asyncpg
import json
import uuid
from datetime import datetime
from typing import Optional
from shared.config import settings
from shared.models import TelegramUpdate, Event
from shared.logger import get_logger

logger = get_logger(__name__)


class EventStore:
    """PostgreSQL-based event store."""
    
    _pool: Optional[asyncpg.Pool] = None
    
    @classmethod
    async def init_pool(cls):
        """Initialize connection pool."""
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                settings.DATABASE_URL,
                min_size=2,
                max_size=20
            )
            logger.info("Event store connection pool initialized")
    
    @classmethod
    async def close_pool(cls):
        """Close connection pool."""
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
            logger.info("Event store connection pool closed")
    
    @classmethod
    async def store_event(cls, update: TelegramUpdate) -> Optional[str]:
        """
        Store Telegram update as event in PostgreSQL.
        
        Returns event_id if successful, None otherwise.
        """
        if not cls._pool:
            await cls.init_pool()
        
        event_id = str(uuid.uuid4())
        
        try:
            async with cls._pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO events 
                    (event_id, event_type, bot_id, user_id, data, 
                     timestamp, source_service)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """,
                    event_id,
                    "telegram_update",
                    update.bot_id,
                    update.user_id,
                    json.dumps(update.dict()),
                    update.timestamp,
                    "gateway"
                )
            
            logger.info(f"Event {event_id} stored from bot {update.bot_id}")
            return event_id
            
        except Exception as e:
            logger.error(f"Error storing event for bot {update.bot_id}: {e}")
            return None


async def initialize_event_store():
    """Initialize event store at app startup."""
    await EventStore.init_pool()
    await create_tables()


async def close_event_store():
    """Close event store at app shutdown."""
    await EventStore.close_pool()


async def create_tables():
    """Create necessary tables if they don't exist."""
    if not EventStore._pool:
        await EventStore.init_pool()
    
    async with EventStore._pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                event_id UUID NOT NULL UNIQUE,
                event_type VARCHAR(50) NOT NULL,
                bot_id VARCHAR(50) NOT NULL,
                user_id BIGINT,
                data JSONB NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                source_service VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_bot_id (bot_id),
                INDEX idx_user_id (user_id),
                INDEX idx_timestamp (timestamp)
            )
            """
        )
        logger.info("Events table created or verified")
