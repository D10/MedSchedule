from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get("/liveness", summary="liveness-проба")
async def get_liveness() -> Response:
    return Response(status_code=status.HTTP_200_OK)
