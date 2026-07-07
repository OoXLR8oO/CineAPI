from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.exceptions import (
    sqlalchemy_exception_handler,
    validation_exception_handler,
)
from app.routes import router

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug,
)


app.include_router(router)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    SQLAlchemyError,
    sqlalchemy_exception_handler,
)


@app.get("/")
async def root():
    return {"message": "Welcome to CineAPI!"}
