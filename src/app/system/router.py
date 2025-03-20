from fastapi import APIRouter

from .health_check import router as health_check_router
from .health_check_readiness import router as health_check_readiness_router

router = APIRouter(prefix="/system", tags=["System"])

router.include_router(health_check_router)
router.include_router(health_check_readiness_router)
