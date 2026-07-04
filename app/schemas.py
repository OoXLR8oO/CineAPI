from datetime import datetime

from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    director: str = Field(min_length=1, max_length=255)
    release_year: int = Field(ge=1888, le=2100)
    genre: str = Field(min_length=1, max_length=100)


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    director: str | None = Field(default=None, min_length=1, max_length=255)
    release_year: int | None = Field(default=None, ge=1888, le=2100)
    genre: str | None = Field(default=None, min_length=1, max_length=100)


class MovieRead(MovieBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
