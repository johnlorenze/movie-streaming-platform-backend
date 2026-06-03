from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.users import User
from app.services.watchlist_service import WatchlistService
from app.api.deps import get_current_user
from app.schemas.watchlist import (
    AddToWatchlistRequest,
    AddOrRemoveToWatchlistResponse,
    GetFromWatchlistResponse
)

router = APIRouter(
    prefix="/watchlist",
    tags=["watchlist"]
)

@router.post(
    "/",
    summary="Add a movie to the user's watchlist",
    description="Adds a specified movie to the authenticated user's watchlist",
    status_code=status.HTTP_201_CREATED,
    response_model=AddOrRemoveToWatchlistResponse
)
async def add_to_watchlist(
    payload: AddToWatchlistRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> AddOrRemoveToWatchlistResponse:
    user_id = current_user.id
    movie_id = payload.movie_id

    watchlist_service = WatchlistService(db)

    return await watchlist_service.add_to_watchlist(user_id, movie_id)

@router.get(
    "/",
    summary="Get the user's watchlist",
    description="Retrieves the authenticated user's watchlist",
    status_code=status.HTTP_200_OK,
    response_model=GetFromWatchlistResponse
)
async def get_watchlist(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> GetFromWatchlistResponse:
    user_id = current_user.id

    watchlist_service = WatchlistService(db)

    return await watchlist_service.get_watchlist(user_id)

@router.delete(
    "/{movie_id}",
    summary="Remove a movie from the user's watchlist",
    description="Removes a specified movie from the authenticated user's watchlist",
    status_code=status.HTTP_200_OK,
    response_model=AddOrRemoveToWatchlistResponse
)
async def remove_from_watchlist(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> AddOrRemoveToWatchlistResponse:
    user_id = current_user.id

    watchlist_service = WatchlistService(db)

    return await watchlist_service.remove_from_watchlist(user_id, movie_id)
