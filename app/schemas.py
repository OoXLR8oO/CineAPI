from pydantic import BaseModel, ConfigDict, Field


class MovieBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    director: str = Field(min_length=1, max_length=255)
    release_year: int = Field(ge=1888, le=2100)
    genre: str = Field(min_length=1, max_length=100)


class MovieCreate(MovieBase):
    pass


class MovieRead(MovieBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    director: str | None = Field(default=None, min_length=1, max_length=255)
    release_year: int | None = Field(default=None, ge=1888, le=2100)
    genre: str | None = Field(default=None, min_length=1, max_length=100)


class MovieFilters(BaseModel):
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    director: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    release_year: int | None = Field(
        default=None,
        ge=1888,
        le=2100,
    )

    genre: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
