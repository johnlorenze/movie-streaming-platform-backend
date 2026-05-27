import re
from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator

PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v) -> str:
        if not PASSWORD_REGEX.match(v):
            raise ValueError("Password must be at least 8 characters long and "
                "contain at least one uppercase letter, one lowercase letter, "
                "one digit, and one special character."
            )
        return v

class RegisterResponse(BaseModel):
    message: str
    user_id: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool

    model_config = {
        "from_attributes": True
    }