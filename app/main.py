from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine
from app.api.v1.api import api_router
from app.core.exception_handlers import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    # Shutdown
    await engine.dispose()

app = FastAPI(title="Movie Streaming Platform", version="1.0", lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")

register_exception_handlers(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}