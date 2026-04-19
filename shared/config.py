"""Shared configuration for all services."""
import os
from typing import Optional


class Settings:
    """Application settings from environment variables."""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@postgres:5432/bott"
    )
    
    # Redis
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://redis:6379/0"
    )
    
    # Service URLs
    GATEWAY_URL: str = os.getenv("GATEWAY_URL", "http://gateway:8000")
    REGISTRY_URL: str = os.getenv("REGISTRY_URL", "http://registry:8001")
    FLOW_ENGINE_URL: str = os.getenv("FLOW_ENGINE_URL", "http://flow-engine:8002")
    TEMPLATE_SERVICE_URL: str = os.getenv("TEMPLATE_SERVICE_URL", "http://template-service:8003")
    DISPATCHER_URL: str = os.getenv("DISPATCHER_URL", "http://dispatcher:8004")
    ANALYTICS_URL: str = os.getenv("ANALYTICS_URL", "http://analytics:8005")
    ADMIN_PANEL_URL: str = os.getenv("ADMIN_PANEL_URL", "http://admin-panel:8006")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Environment
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"


settings = Settings()
