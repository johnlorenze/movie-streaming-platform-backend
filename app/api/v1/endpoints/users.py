from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    TokenResponse,
    UserResponse
)
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.core.constants.summary_and_descriptions import SummaryAndDescriptions

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post(
    "/register",
    summary=SummaryAndDescriptions.SUMM_REGISTER,
    description=SummaryAndDescriptions.DESC_REGISTER,
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse
)
async def register(payload: RegisterRequest, db: AsyncSession=Depends(get_db)) -> TokenResponse:
    """Creates a user in the system"""

    auth_service = AuthService(db)

    return await auth_service.register_user(str(payload.email), payload.password)

@router.post(
    "/login",
    summary=SummaryAndDescriptions.SUMM_LOGIN,
    description=SummaryAndDescriptions.DESC_LOGIN,
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse
)
async def login_user(payload: LoginRequest, db: AsyncSession=Depends(get_db)) -> TokenResponse:
    """Authenticates a user in the system"""

    auth_service = AuthService(db)

    return await auth_service.login_user(str(payload.email), payload.password)

@router.get(
    "/me",
    summary=SummaryAndDescriptions.SUMM_ME,
    description=SummaryAndDescriptions.DESC_ME,
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def me(current_user=Depends(get_current_user)) -> UserResponse:
    return current_user