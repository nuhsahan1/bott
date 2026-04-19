"""Registry service - Bot configuration management."""
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

router = APIRouter()


@router.get("/bots")
async def list_bots():
    """List all registered bots."""
    return {"bots": []}


@router.get("/bots/{bot_id}")
async def get_bot(bot_id: str):
    """Get bot configuration."""
    return {"bot_id": bot_id, "status": "active"}


@router.post("/bots")
async def register_bot():
    """Register new bot."""
    return {"status": "created"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle."""
    print("Registry service starting...")
    yield
    print("Registry service stopping...")


app = FastAPI(title="Bot Registry Service", lifespan=lifespan)
app.include_router(router, prefix="/api", tags=["registry"])


@app.get("/")
async def root():
    return {"service": "registry", "status": "running"}
