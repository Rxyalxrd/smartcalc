from fastapi import APIRouter
from app.api.routers.user import router as user_router
from app.api.enpoints import compute_construction, get_history

main_router = APIRouter()

main_router.include_router(user_router)

main_router.include_router(
    compute_construction,
    prefix='/compute_construction',
    tags=('Compute construction',)
)

main_router.include_router(
    get_history,
    prefix='/get_history',
    tags=('Get history',)
)
