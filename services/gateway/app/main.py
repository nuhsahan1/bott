"""Gateway service main application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from shared.logger import get_logger
from .routes import router
from .event_store import initialize_event_store, close_event_store

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown."""
    # Startup
    logger.info("Gateway service starting...")
    await initialize_event_store()
    logger.info("Gateway service ready")
    yield
    # Shutdown
    logger.info("Gateway service shutting down...")
    await close_event_store()
    logger.info("Gateway service stopped")


# Create FastAPI app
app = FastAPI(
    title="Telegram Multi-Bot Gateway",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api", tags=["webhook"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "gateway",
        "status": "running",
        "version": "0.1.0"
    }
