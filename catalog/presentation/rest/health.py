import logging

from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health():
    logger.info("Health check")
    return {"status": "ok"}
