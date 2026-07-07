from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Movie
from app.repositories import movie_repository
from app.schemas import MovieCreate, MovieFilters, MovieUpdate


async def list_movies(db: AsyncSession, filters: MovieFilters) -> list[Movie]:
    return await movie_repository.list_movies(db, filters)


async def get_movie_or_404(
    db: AsyncSession,
    movie_id: int,
) -> Movie:
    movie = await movie_repository.get_movie(db, movie_id)

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    return movie


async def create_movie(db: AsyncSession, payload: MovieCreate) -> Movie:
    return await movie_repository.create_movie(db, payload)


async def update_movie(
    db: AsyncSession,
    movie_id: int,
    payload: MovieUpdate,
) -> Movie:
    movie = await movie_repository.get_movie(db, movie_id)

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    return await movie_repository.update_movie(db, movie, payload)


async def delete_movie(
    db: AsyncSession,
    movie_id: int,
) -> None:
    movie = await get_movie_or_404(db, movie_id)

    await movie_repository.delete_movie(db, movie)
