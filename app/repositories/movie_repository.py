from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Movie
from app.schemas import MovieCreate, MovieFilters, MovieUpdate


async def list_movies(db: AsyncSession, filters: MovieFilters) -> list[Movie]:
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


async def get_movie(db: AsyncSession, movie_id: int) -> Movie | None:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))

    return result.scalar_one_or_none()


async def create_movie(db: AsyncSession, movie_data: MovieCreate) -> Movie:
    movie = Movie(**movie_data.model_dump())

    db.add(movie)

    await db.commit()
    await db.refresh(movie)

    return movie


async def update_movie(
    db: AsyncSession,
    movie: Movie,
    movie_data: MovieUpdate,
) -> Movie:
    updates = movie_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(movie, field, value)

    await db.commit()
    await db.refresh(movie)

    return movie


async def delete_movie(db: AsyncSession, movie: Movie) -> None:
    await db.delete(movie)
    await db.commit()
