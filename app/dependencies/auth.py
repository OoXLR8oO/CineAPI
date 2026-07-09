from logging import getLogger

from fastapi import Header, HTTPException, status

from app.config import settings

logger = getLogger(__name__)


async def verify_admin_key(
    x_api_key: str = Header(),
):
    if x_api_key != settings.api_key:
        logger.warning("Failed admin authentication attempt")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return True
