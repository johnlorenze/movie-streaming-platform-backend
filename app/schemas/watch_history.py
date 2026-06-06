from uuid import UUID
from pydantic import BaseModel, Field

class AddToWatchHistoryRequest(BaseModel):
    movie_id: int

class AddToOrRemoveFromWatchHistoryResponse(BaseModel):
    message: str = Field(min_length=1)

class GetFromWatchHistoryResponse(BaseModel):
    movie_ids: list[int]