"""Telegram update normalization logic."""
from typing import Optional, Dict, Any
from datetime import datetime
from shared.models import TelegramUpdate
from shared.logger import get_logger

logger = get_logger(__name__)


def normalize_update(raw_update: Dict[str, Any], bot_id: str) -> Optional[TelegramUpdate]:
    """
    Normalize raw Telegram update to TelegramUpdate model.
    
    Extracts relevant fields from Telegram Bot API update format.
    Handles different message types (text, photo, video, etc.).
    """
    try:
        update_id = raw_update.get("update_id")
        message = raw_update.get("message", {})
        
        if not message:
            logger.warning(f"No message in update {update_id} for bot {bot_id}")
            return None
        
        user = message.get("from", {})
        chat = message.get("chat", {})
        
        # Determine message type
        message_type = "text"
        if "photo" in message:
            message_type = "photo"
        elif "video" in message:
            message_type = "video"
        elif "document" in message:
            message_type = "document"
        elif "audio" in message:
            message_type = "audio"
        elif "sticker" in message:
            message_type = "sticker"
        
        normalized = TelegramUpdate(
            bot_id=bot_id,
            update_id=update_id,
            user_id=user.get("id"),
            chat_id=chat.get("id"),
            message_text=message.get("text"),
            message_type=message_type,
            raw_payload=raw_update,
            timestamp=datetime.utcnow()
        )
        
        logger.info(
            f"Normalized update {update_id} from user {normalized.user_id} "
            f"in bot {bot_id} ({message_type})"
        )
        return normalized
        
    except Exception as e:
        logger.error(f"Error normalizing update for bot {bot_id}: {e}")
        return None
