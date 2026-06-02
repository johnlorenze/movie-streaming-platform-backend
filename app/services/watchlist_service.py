from fastapi import HTTPException, status
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.watchlists import WatchList
from app.schemas.watchlist import AddOrRemoveToWatchlistResponse, GetFromWatchlistResponse
from app.repositories.watchlist_repository import WatchlistRepository

class WatchlistService:
    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db
        self.watchlist_repository = WatchlistRepository(db)

    async def add_to_watchlist(self, user_id: UUID, movie_id: int) -> AddOrRemoveToWatchlistResponse:
        try:
            new_entry = WatchList(
                user_id=user_id,
                movie_id=movie_id
            )

            await self.watchlist_repository.add_to_watchlist(new_entry)
            await self.db.commit()
            await self.db.refresh(new_entry)

            return AddOrRemoveToWatchlistResponse(
                message="Movie added to watchlist successfully"
            )
        except IntegrityError as e:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Movie already exists in watchlist",
            ) from e
        except Exception as e:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add movie to watchlist"
            ) from e

    async def get_watchlist(self, user_id: UUID) -> GetFromWatchlistResponse:
        result = await self.watchlist_repository.get_watchlist(user_id)
        movie_ids = [entry.movie_id for entry in result]

        return GetFromWatchlistResponse(movie_ids=movie_ids)

    async def remove_from_watchlist(self, user_id: UUID, movie_id: int) -> AddOrRemoveToWatchlistResponse:
        try:
            await self.watchlist_repository.remove_from_watchlist(user_id, movie_id)
            await self.db.commit()

            return AddOrRemoveToWatchlistResponse(
                message="Movie removed from watchlist successfully"
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found in watchlist"
            ) from e
        except Exception as e:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove movie from watchlist"
            ) from e
