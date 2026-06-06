from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.watch_history_repository import WatchHistoryRepository
from app.db.models.watch_history import WatchHistory
from app.schemas.watch_history import AddToOrRemoveFromWatchHistoryResponse, GetFromWatchHistoryResponse

class WatchHistoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.watch_history_repository = WatchHistoryRepository(db)

    async def add_watch_history(self, user_id: UUID, movie_id: int):
        try:
            new_entry = WatchHistory(
                user_id=user_id,
                movie_id=movie_id
            )

            await self.watch_history_repository.add_watch_history(new_entry)
            await self.db.commit()
            await self.db.refresh(new_entry)

            return AddToOrRemoveFromWatchHistoryResponse(
                message=f"Movie {movie_id} added to watch history for user {user_id}"
            )
        except IntegrityError as e:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Movie already exists in watch history"
            ) from e
        except Exception as e:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add movie to watch history"
            ) from e

    async def get_watch_history(self, user_id: UUID) -> GetFromWatchHistoryResponse:
        try:
            result = await self.watch_history_repository.get_watch_history(user_id)
            movie_ids = [entry.movie_id for entry in result]

            return GetFromWatchHistoryResponse(movie_ids=movie_ids)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to retrieve watch history"
            ) from e

    async def remove_watch_history(self, user_id: UUID, movie_id: int):
        try:
            await self.watch_history_repository.remove_from_watch_history(user_id, movie_id)
            await self.db.commit()

            return AddToOrRemoveFromWatchHistoryResponse(
                message=f"Movie {movie_id} removed from watch history for user {user_id}"
            )
        except ValueError as e:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found in watch history",
            ) from e
        except Exception as e:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove movie from watch history"
            ) from e