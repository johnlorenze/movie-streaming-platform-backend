from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.users import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.db.scalar(
            select(User).where(User.email == email)
        )

    async def create_user(self, user: User):
        self.db.add(user)