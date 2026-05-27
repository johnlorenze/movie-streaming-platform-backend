import logging
from fastapi import HTTPException, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select
from app.core.security import hash_password, verify_password, create_access_token
from app.db.models import User
from app.schemas.auth import RegisterResponse, TokenResponse
# from app.schemas.user import UserOut
# from app.db.transaction import transaction

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db):
        self.db = db

    async def register_user(self, email: str, password: str) -> RegisterResponse:
        is_existing_user = await self.db.scalar(
            select(User).where(User.email == email)
        )

        print("is_existing_user:", is_existing_user)

        if is_existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            email=email,
            hashed_password=await run_in_threadpool(hash_password, password),
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return RegisterResponse(
            message="User registered successfully",
            user_id=str(user.id)
        )

    async def login_user(self, email: str, password: str) -> TokenResponse:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

        user = await self.db.scalar(
            select(User).where(User.email == email)
        )

        if not user or not user.is_active:
            raise credentials_exception

        is_valid_password = await run_in_threadpool(verify_password, password, user.hashed_password)

        if not is_valid_password:
            raise credentials_exception

        access_token = create_access_token(str(user.id))

        return TokenResponse(
            access_token=access_token
        )