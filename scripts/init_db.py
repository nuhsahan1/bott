"""Database initialization and migrations."""
import asyncio
import asyncpg
from shared.config import settings
from shared.logger import get_logger

logger = get_logger(__name__)


async def init_database():
    """Initialize PostgreSQL database and create tables."""
    try:
        # Connect to default postgres database
        conn = await asyncpg.connect(
            host="postgres",
            user="postgres",
            password="password",
            database="postgres"
        )
        
        databases = await conn.fetch("SELECT datname FROM pg_database WHERE datname = 'bott'")
        
        if not databases:
            await conn.execute("CREATE DATABASE bott")
            logger.info("Created 'bott' database")
        
        await conn.close()
        
        # Connect to bott database and create tables
        conn = await asyncpg.connect(settings.DATABASE_URL)
        
        # Create events table
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
            );
            CREATE INDEX IF NOT EXISTS idx_events_bot_id ON events(bot_id);
            CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id);
            CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
            """
        )
        logger.info("Events table created")
        
        # Create bots table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bots (
                id SERIAL PRIMARY KEY,
                bot_id VARCHAR(50) NOT NULL UNIQUE,
                bot_token VARCHAR(255) NOT NULL,
                bot_name VARCHAR(100) NOT NULL,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_bots_bot_id ON bots(bot_id);
            """
        )
        logger.info("Bots table created")
        
        # Create flows table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS flows (
                id SERIAL PRIMARY KEY,
                bot_id VARCHAR(50) NOT NULL,
                flow_name VARCHAR(100) NOT NULL,
                definition JSONB NOT NULL,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bot_id) REFERENCES bots(bot_id),
                INDEX idx_flows_bot_id (bot_id)
            );
            CREATE INDEX IF NOT EXISTS idx_flows_bot_id ON flows(bot_id);
            """
        )
        logger.info("Flows table created")
        
        await conn.close()
        logger.info("Database initialization complete")
        
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_database())
