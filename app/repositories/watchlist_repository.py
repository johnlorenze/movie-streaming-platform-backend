from typing import Any, Sequence
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.watchlists import WatchList

class WatchlistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_to_watchlist(self, new_entry: WatchList):
        self.db.add(new_entry)

    async def get_watchlist(self, user_id: UUID) -> Sequence[WatchList]:
        watchlist = await self.db.scalars(
            select(WatchList).where(WatchList.user_id == user_id)
        )

        return watchlist.all()

    async def remove_from_watchlist(self, user_id: UUID, movie_id: int) -> None:
        entry = await self.db.scalar(
            select(WatchList).where(
                WatchList.user_id == user_id,
                WatchList.movie_id == movie_id
            )
        )

        if entry:
            await self.db.delete(entry)
        else:
            raise ValueError("Movie not found in watchlist")

