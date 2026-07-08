from logging import getLogger

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

logger = getLogger(__name__)


async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": exception.errors()},
    )


async def sqlalchemy_exception_handler(
    request: Request,
    exception: SQLAlchemyError,
) -> JSONResponse:
    logger.exception(
        "Unhandled SQLAlchemy exception on %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )


async def integrity_error_exception_handler(
    request: Request,
    exception: IntegrityError,
) -> JSONResponse:
    logger.exception(
        "Database integrity error on %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "The request conflicts with existing data."},
    )
