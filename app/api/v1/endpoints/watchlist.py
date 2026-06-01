from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.users import User
from app.services.watchlist_service import WatchlistService
from app.api.deps import get_current_user
from app.schemas.watchlist import AddToWatchlistRequest, AddOrRemoveToWatchlistResponse

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
    print(f"Adding movie with ID {movie_id} to watchlist for user ID {user_id}")
    watchlist_service = WatchlistService(db)

    return await watchlist_service.add_to_watchlist(user_id, movie_id)
