"""Template Service - Message template management."""
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

router = APIRouter()


@router.get("/templates/{bot_id}")
async def get_templates(bot_id: str):
    """Get bot's message templates."""
    return {"bot_id": bot_id, "templates": []}


@router.post("/render")
async def render_template():
    """Render template with variables."""
    return {"rendered": "Hello {{name}}!"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle."""
    print("Template Service starting...")
    yield
    print("Template Service stopping...")


app = FastAPI(title="Template Service", lifespan=lifespan)
app.include_router(router, prefix="/api", tags=["template"])


@app.get("/")
async def root():
    return {"service": "template-service", "status": "running"}
