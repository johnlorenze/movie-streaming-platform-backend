from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.watchlists import WatchList

class WatchlistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_to_watchlist(self, new_entry: WatchList):
        self.db.add(new_entry)

    # async def remove_from_watchlist(self, user_id, movie_id):
    #     entry = await self.db.scalar(
    #         select(WatchList).where(
    #             WatchList.user_id == user_id,
    #             WatchList.movie_id == movie_id
    #         )
    #     )
    #     if entry:
    #         await self.db.delete(entry)
    #         await self.db.commit()
    #
    # async def get_watchlist(self, user_id):
    #     return await self.db.scalars(
    #         select(WatchList).where(WatchList.user_id == user_id)
    #     ).all()