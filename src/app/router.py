from fastapi import APIRouter

from .system.router import router as system_router
from .v1.router import router as router_v1

router = APIRouter(prefix="/api")

router.include_router(system_router)
router.include_router(router_v1)
