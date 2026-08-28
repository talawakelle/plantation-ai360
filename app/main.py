from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.routes import health, master, operations, weather, vision, ai, ingest, dashboard

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, docs_url="/docs", redoc_url="/redoc")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(health.router, prefix="/api/v1")
app.include_router(master.router, prefix="/api/v1/master")
app.include_router(operations.router, prefix="/api/v1/operations")
app.include_router(weather.router, prefix="/api/v1/weather")
app.include_router(vision.router, prefix="/api/v1/vision")
app.include_router(ai.router, prefix="/api/v1/ai")
app.include_router(ingest.router, prefix="/api/v1/ingest")
app.include_router(dashboard.router, prefix="/api/v1/dashboard")

static_dir = Path(__file__).resolve().parent.parent / "frontend"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=static_dir), name="assets")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(static_dir / "index.html")
