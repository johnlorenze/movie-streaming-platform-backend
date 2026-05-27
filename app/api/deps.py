from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_access_token
from app.db.database import get_db
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

async def get_current_user(
        token: str=Depends(oauth2_scheme),
        db: AsyncSession=Depends(get_db)
) -> User:
    """Retrieves the current user based on the provided JWT token"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_uuid = UUID(user_id)
        user = await db.scalar(
            select(User).where(User.id == user_uuid)
        )

        if user is None:
            raise credentials_exception

        return user
    except (JWTError, ValueError, TypeError):
        raise credentials_exception