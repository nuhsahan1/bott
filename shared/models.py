"""Shared models across all services."""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class TelegramUpdate(BaseModel):
    """Normalized Telegram update message."""
    bot_id: str
    update_id: Optional[int] = None
    user_id: Optional[int] = None
    chat_id: Optional[int] = None
    message_text: Optional[str] = None
    message_type: str = "text"  # text, photo, video, etc.
    raw_payload: Dict[str, Any]
    timestamp: datetime


class BotConfig(BaseModel):
    """Bot configuration model."""
    bot_id: str
    bot_token: str
    bot_name: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class FlowDecision(BaseModel):
    """Flow engine decision."""
    bot_id: str
    user_id: int
    action: str  # e.g., "send_message", "store_session", "route_to_service"
    target_service: Optional[str] = None
    payload: Dict[str, Any]
    priority: int = 0


class Event(BaseModel):
    """Event store model."""
    event_id: str
    event_type: str
    bot_id: str
    user_id: Optional[int] = None
    data: Dict[str, Any]
    timestamp: datetime
    source_service: str
