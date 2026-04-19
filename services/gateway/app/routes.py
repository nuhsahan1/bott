"""Gateway service webhook routes."""
from fastapi import APIRouter, Request, HTTPException
from shared.models import TelegramUpdate
from shared.logger import get_logger
from .normalization import normalize_update
from .event_store import EventStore
from .flow_engine import forward_to_flow_engine

logger = get_logger(__name__)
router = APIRouter()


@router.post("/webhook/{bot_id}")
async def handle_webhook(bot_id: str, request: Request):
    """
    Handle incoming Telegram webhook update.
    
    Flow:
    1. Receive raw update from Telegram
    2. Extract bot_id from path
    3. Normalize payload
    4. Store event in PostgreSQL
    5. Forward to flow engine for processing
    """
    
    # 1. Receive and parse update
    try:
        raw_update = await request.json()
    except Exception as e:
        logger.warning(f"Invalid JSON received for bot {bot_id}: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    logger.debug(f"Received update for bot {bot_id}: {raw_update.get('update_id')}")
    
    # 2. Normalize payload
    normalized = normalize_update(raw_update, bot_id)
    if not normalized:
        logger.warning(f"Failed to normalize update for bot {bot_id}")
        raise HTTPException(status_code=400, detail="Could not normalize update")
    
    # 3. Store event
    event_id = await EventStore.store_event(normalized)
    if not event_id:
        logger.error(f"Failed to store event for bot {bot_id}")
        raise HTTPException(status_code=500, detail="Failed to store event")
    
    # 4. Forward to flow engine (non-blocking)
    success = await forward_to_flow_engine(normalized)
    if not success:
        logger.warning(f"Failed to forward update to flow engine for bot {bot_id}")
        # Don't fail the webhook response - event is already stored
    
    return {
        "status": "ok",
        "event_id": event_id,
        "bot_id": bot_id,
        "update_id": normalized.update_id
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "gateway"}
