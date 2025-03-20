from fastapi import APIRouter

from .schedule import router as schedule_router

router = APIRouter(prefix="/v1")

router.include_router(schedule_router)
