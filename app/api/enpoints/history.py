import json
import logging

from fastapi import APIRouter, Depends, Request, status
import redis.asyncio as aioredis

from app.core.redis_db import get_redis_connection
from app.core.auth import current_user
from app.models.user import User
from app.schemas.compute_construction import ComputeConstructionRead
from app.schemas.error import ErrorResponse
from app.exceptions.exceptions import message_exception_handler
from app.loggers.log import setup_logging
from app.utils.const.load_yaml_const import open_yaml


setup_logging()
logger = logging.getLogger(__name__)
router = APIRouter()

error_history_message = open_yaml("exception_const.yaml")


@router.get(
    '/get_history',
    response_model=(
        list[ComputeConstructionRead] |
        ComputeConstructionRead |
        ErrorResponse
    ),
    response_model_exclude_none=True,
    dependencies=(Depends(current_user),)
)
@message_exception_handler(
    log_error_text=error_history_message["history_log_error_text"],
    message_error_text=error_history_message["history_message_error_text"]
)
async def get_history(
    request: Request,
    current_user: User = Depends(current_user),
    redis: aioredis.Redis = Depends(get_redis_connection)
) -> list[ComputeConstructionRead] | ComputeConstructionRead | ErrorResponse:

    """
    Только для пользователей.

    Возвращает результаты и вводимые данные одного или
    нескольких элементов конструкции. Для каждого
    пользователя своя история.
    """

    redis_key = f"user_{current_user.id}"

    existing_data = await redis.get(redis_key)

    if not existing_data:
        return ErrorResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=error_history_message["history_message_not_content"]
        )

    parsed_data = json.loads(existing_data)

    logger.info(f"Пользователь {redis_key} получил историю запросов.")

    return parsed_data
