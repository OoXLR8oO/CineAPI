from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

import app.logging_config  # noqa: F811
from app.config import settings
from app.exceptions import (
    integrity_error_exception_handler,
    sqlalchemy_exception_handler,
    validation_exception_handler,
)
from app.routes import admin_router, public_router

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug,
)


app.include_router(admin_router)
app.include_router(public_router)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    SQLAlchemyError,
    sqlalchemy_exception_handler,
)

app.add_exception_handler(
    IntegrityError,
    integrity_error_exception_handler,
)


@app.get("/")
async def root():
    return {"message": "Welcome to CineAPI!"}
