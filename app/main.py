from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    # Shutdown
    await engine.dispose()

app = FastAPI(title="Movie Streaming Platform", version="1.0", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}