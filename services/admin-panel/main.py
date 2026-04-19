"""Admin Panel service - Configuration and management."""
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

router = APIRouter()


@router.get("/dashboard")
async def admin_dashboard():
    """Admin dashboard."""
    return {"status": "ok", "services": []}


@router.get("/users")
async def list_users():
    """List admin users."""
    return {"users": []}


@router.post("/settings")
async def update_settings():
    """Update system settings."""
    return {"status": "updated"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle."""
    print("Admin Panel service starting...")
    yield
    print("Admin Panel service stopping...")


app = FastAPI(title="Admin Panel Service", lifespan=lifespan)
app.include_router(router, prefix="/api", tags=["admin"])


@app.get("/")
async def root():
    return {"service": "admin-panel", "status": "running"}
