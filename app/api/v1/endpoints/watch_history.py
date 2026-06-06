from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.users import User
from app.services.watch_history_service import WatchHistoryService
from app.api.deps import get_current_user
from app.schemas.watch_history import (
    AddToWatchHistoryRequest,
    AddToOrRemoveFromWatchHistoryResponse,
    GetFromWatchHistoryResponse
)

router = APIRouter(
    prefix="/watch-history",
    tags=["watch-history"]
)

@router.post(
    "/",
    summary="Add video to watch history",
    description="Add a video to the user's watch history",
    status_code=status.HTTP_201_CREATED,
    response_model=AddToOrRemoveFromWatchHistoryResponse
)
async def add_to_watch_history(
    payload: AddToWatchHistoryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> AddToOrRemoveFromWatchHistoryResponse:
    user_id = current_user.id
    movie_id = payload.movie_id

    watch_history_service = WatchHistoryService(db)

    return await watch_history_service.add_watch_history(user_id, movie_id)

@router.get(
    "/",
    summary="Get watch history",
    description="Get the user's watch history",
    status_code=status.HTTP_200_OK,
    response_model=GetFromWatchHistoryResponse
)
async def get_watch_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> GetFromWatchHistoryResponse:
    user_id = current_user.id

    watch_history_service = WatchHistoryService(db)

    return await watch_history_service.get_watch_history(user_id)

@router.delete(
    "/{movie_id}",
    summary="Remove video from watch history",
    description="Remove a video from the user's watch history",
    status_code=status.HTTP_200_OK,
    response_model=AddToOrRemoveFromWatchHistoryResponse
)
async def remove_from_watch_history(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> AddToOrRemoveFromWatchHistoryResponse:
    user_id = current_user.id

    watch_history_service = WatchHistoryService(db)

    return await watch_history_service.remove_watch_history(user_id, movie_id)