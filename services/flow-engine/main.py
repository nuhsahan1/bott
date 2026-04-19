"""Flow Engine service - Decision engine for bot flows."""
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

router = APIRouter()


@router.post("/process_update")
async def process_update():
    """Process Telegram update and make flow decisions."""
    return {"status": "processed", "decision": "forward_to_template"}


@router.get("/flows/{bot_id}")
async def get_flows(bot_id: str):
    """Get bot's configured flows."""
    return {"bot_id": bot_id, "flows": []}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle."""
    print("Flow Engine service starting...")
    yield
    print("Flow Engine service stopping...")


app = FastAPI(title="Flow Engine Service", lifespan=lifespan)
app.include_router(router, prefix="/api", tags=["flow"])


@app.get("/")
async def root():
    return {"service": "flow-engine", "status": "running"}
