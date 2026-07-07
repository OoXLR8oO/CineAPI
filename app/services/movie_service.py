from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Movie
from app.schemas import MovieFilters


async def get_movie_or_404(
    db: AsyncSession,
    movie_id: int,
) -> Movie:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    return movie


async def list_movies(
    db: AsyncSession,
    filters: MovieFilters,
) -> list[Movie]:
    conditions = []

    if filters.title:
        conditions.append(Movie.title.ilike(f"%{filters.title}%"))

    if filters.director:
        conditions.append(Movie.director.ilike(f"%{filters.director}%"))

    if filters.release_year:
        conditions.append(Movie.release_year == filters.release_year)

    if filters.genre:
        conditions.append(Movie.genre.ilike(f"%{filters.genre}%"))

    query = (
        select(Movie)
        .where(*conditions)
        .order_by(Movie.id)
        .limit(filters.limit)
        .offset(filters.offset)
    )

    result = await db.execute(query)

    return result.scalars().all()
