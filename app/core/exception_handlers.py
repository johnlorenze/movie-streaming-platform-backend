from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    EmailAlreadyRegisteredException,
    InvalidCredentialsException,
)

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(EmailAlreadyRegisteredException)
    async def email_exists_handler(
        request: Request,
        exc: EmailAlreadyRegisteredException,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Email already registered"
            },
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsException,
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": "Invalid credentials"
            },
        )