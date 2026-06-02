import logging
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, verify_password, create_access_token
from app.db.models.users import User
from app.schemas.auth import RegisterResponse, TokenResponse
from app.core.exceptions import EmailAlreadyRegisteredException, InvalidCredentialsException
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db
        self.user_repository = UserRepository(db)

    @staticmethod
    def _build_token_response(user: User) -> TokenResponse:
        access_token = create_access_token(str(user.id))

        return TokenResponse(
            access_token=access_token,
            user_id=user.id,
            email=user.email
        )

    async def register_user(self, email: str, password: str) -> TokenResponse:
        user = User(
            email=email,
            hashed_password=await run_in_threadpool(hash_password, password),
        )

        async with self.db.begin():
            is_existing_user = await self.user_repository.get_user_by_email(email)

            logger.debug("Checking for existing user during registration")

            if is_existing_user:
                raise EmailAlreadyRegisteredException()

            await self.user_repository.create_user(user)

        await self.db.refresh(user)

        return self._build_token_response(user)

    async def login_user(self, email: str, password: str) -> TokenResponse:
        user = await self.user_repository.get_user_by_email(email)

        if not user or not user.is_active:
            raise InvalidCredentialsException()

        is_valid_password = await run_in_threadpool(verify_password, password, user.hashed_password)

        if not is_valid_password:
            raise InvalidCredentialsException()

        return self._build_token_response(user)