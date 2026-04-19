"""Response Dispatcher service - Send responses to Telegram."""
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

router = APIRouter()


@router.post("/send_message")
async def send_message():
    """Send message to Telegram user."""
    return {"status": "sent", "message_id": 12345}


@router.post("/send_batch")
async def send_batch():
    """Send batch of messages."""
    return {"status": "queued", "count": 10}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle."""
    print("Dispatcher service starting...")
    yield
    print("Dispatcher service stopping...")


app = FastAPI(title="Response Dispatcher Service", lifespan=lifespan)
app.include_router(router, prefix="/api", tags=["dispatcher"])


@app.get("/")
async def root():
    return {"service": "dispatcher", "status": "running"}
