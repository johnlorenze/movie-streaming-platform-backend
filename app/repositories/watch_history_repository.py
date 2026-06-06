from typing import Sequence
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.watch_history import WatchHistory

class WatchHistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_watch_history(self, new_entry: WatchHistory):
        self.db.add(new_entry)

    async def get_watch_history(self, user_id: UUID) -> Sequence[WatchHistory]:
        watch_history = await self.db.scalars(
            select(WatchHistory)
            .where(WatchHistory.user_id == user_id)
            .order_by(WatchHistory.watched_at.desc())
        )

        return watch_history.all()

    async def remove_from_watch_history(self, user_id: UUID, movie_id: int) -> None:
        entry = await self.db.scalar(
            select(WatchHistory).where(
                WatchHistory.user_id == user_id,
                WatchHistory.movie_id == movie_id
            )
        )

        if entry:
            await self.db.delete(entry)
        else:
            raise ValueError("Movie not found in watch history")