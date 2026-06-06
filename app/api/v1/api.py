from fastapi import APIRouter
from app.api.v1.endpoints import users, watchlist, movies, watch_history

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(watchlist.router)
api_router.include_router(movies.router)
api_router.include_router(watch_history.router)