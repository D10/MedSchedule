from collections.abc import Awaitable
from typing import Callable

from fastapi import APIRouter
from pydantic import BaseModel, Field, computed_field

from src.adapters.database.health_check import check_database

router = APIRouter()


class AppDependSchema(BaseModel):
    name: str
    ok: bool
    error: str | None = Field(default=None)


class AppReadinesSchema(BaseModel):
    depends: list[AppDependSchema]

    @property
    @computed_field
    def ok(self) -> bool:
        return all(depend.ok for depend in self.depends)


@router.get("/readiness", response_model=AppReadinesSchema, summary="readiness-проба")
async def get_readiness() -> AppReadinesSchema:
    app_readiness = AppReadinesSchema(depends=[])

    app_depends: dict[str, Callable[[], Awaitable[None]]] = {
        "database": check_database,
    }
    for name, check in app_depends.items():
        try:
            await check()
        except Exception as exc:
            depend = AppDependSchema(name=name, ok=False, error=str(exc))
        else:
            depend = AppDependSchema(name=name, ok=True)

        app_readiness.depends.append(depend)

    return app_readiness
