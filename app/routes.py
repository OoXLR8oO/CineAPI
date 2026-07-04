from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Movie
from app.schemas import MovieCreate, MovieRead, MovieUpdate

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/health/db")
async def db_health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(select(1))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@router.get("", response_model=list[MovieRead])
async def list_movies(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    title: Annotated[str | None, Query(min_length=1, max_length=255)] = None,
    director: Annotated[str | None, Query(min_length=1, max_length=255)] = None,
    release_year: Annotated[int | None, Query(ge=1888, le=2100)] = None,
    genre: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Movie)

    if title:
        query = query.where(Movie.title.ilike(f"%{title}%"))

    if director:
        query = query.where(Movie.director.ilike(f"%{director}%"))

    if release_year:
        query = query.where(Movie.release_year == release_year)

    if genre:
        query = query.where(Movie.genre.ilike(f"%{genre}%"))

    query = query.order_by(Movie.id).limit(limit).offset(offset)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{movie_id}", response_model=MovieRead)
async def get_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


@router.post("", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
async def create_movie(
    payload: MovieCreate,
    db: AsyncSession = Depends(get_db),
):
    movie = Movie(**payload.model_dump())
    db.add(movie)

    await db.commit()
    await db.refresh(movie)

    return movie


@router.patch("/{movie_id}", response_model=MovieRead)
async def update_movie(
    movie_id: int,
    payload: MovieUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(movie, field, value)

    await db.commit()
    await db.refresh(movie)

    return movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    await db.delete(movie)
    await db.commit()
