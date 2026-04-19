"""Flow engine service client."""
import httpx
from typing import Optional, Dict, Any
from shared.config import settings
from shared.models import TelegramUpdate
from shared.logger import get_logger

logger = get_logger(__name__)


async def forward_to_flow_engine(update: TelegramUpdate) -> bool:
    """
    Forward normalized update to flow engine for processing.
    
    Returns True if successful, False otherwise.
    """
    url = f"{settings.FLOW_ENGINE_URL}/process_update"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url,
                json=update.dict(),
                headers={"X-Bot-ID": update.bot_id, "Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            logger.info(
                f"Update from bot {update.bot_id} forwarded to flow engine "
                f"(user: {update.user_id})"
            )
            return True
            
    except httpx.ConnectError:
        logger.error(f"Failed to connect to flow engine at {url}")
        return False
    except httpx.TimeoutException:
        logger.error(f"Timeout forwarding update to flow engine")
        return False
    except Exception as e:
        logger.error(f"Error forwarding update to flow engine: {e}")
        return False
