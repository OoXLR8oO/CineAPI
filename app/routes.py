from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Movie
from app.schemas import MovieCreate, MovieFilters, MovieRead, MovieUpdate
from app.services import movie_service

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/health/db")
async def db_health(db: AsyncSession = Depends(get_db)):
    await db.execute(select(1))
    return {"status": "ok"}


@router.get("/debug/error")
async def force_error():
    raise RuntimeError("test error")


@router.get("", response_model=list[MovieRead])
async def list_movies(
    filters: Annotated[MovieFilters, Depends()],
    db: AsyncSession = Depends(get_db),
):
    return await movie_service.list_movies(db, filters)


@router.get("/{movie_id}", response_model=MovieRead)
async def get_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    movie = await movie_service.get_movie_or_404(db, movie_id)

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
    movie = await movie_service.get_movie_or_404(db, movie_id)

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
    movie = await movie_service.get_movie_or_404(db, movie_id)

    await db.delete(movie)
    await db.commit()
