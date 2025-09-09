import logging

from fastapi import APIRouter

from catalog.presentation.rest._base_schemas import SuccessResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health() -> SuccessResponse:
    logger.info("Health check")
    return SuccessResponse()
