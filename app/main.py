from fastapi import FastAPI

from app.api.routers.main_router import main_router
from app.core.config import settings

app = FastAPI(title=settings.app_title, description=settings.app_discription)

app.include_router(main_router)
