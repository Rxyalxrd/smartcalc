import json
import logging

from fastapi import APIRouter, Depends, Request
import redis.asyncio as aioredis

from app.core.redis_db import get_redis_connection
from app.core.auth import current_user
from app.models.user import User
from app.schemas.compute_construction import (
    ComputeConstructionCreate,
    ComputeConstructionsCreate
)
from app.exceptions.exceptions import message_exception_handler
from app.loggers.log import setup_logging
from app.utils.const.load_yaml_const import open_yaml
from app.api.validators.compute_construction import is_existing_data


setup_logging()
logger = logging.getLogger(__name__)
router = APIRouter()

error_compute_message = open_yaml("exception_const.yaml")


@router.post(
    '/create_compute_construction',
    response_model=ComputeConstructionCreate,
    response_model_exclude_none=True,
    dependencies=(Depends(current_user),)
)
@message_exception_handler(
    log_error_text=error_compute_message["construction_log_error_text"],
    message_error_text=error_compute_message["construction_message_error_text"]
)
async def compute_construction(
    request: Request,
    compute_construction: ComputeConstructionCreate,
    current_user: User = Depends(current_user),
    redis: aioredis.Redis = Depends(get_redis_connection)
) -> ComputeConstructionCreate:
    """
    Только для пользователей.

    Теплотехнический расчет одного элемента конструкции.
    Сохраняет расчет в Redis по ключу, основанному на ID пользователя.
    Если запись user_id уже существует, добавляет новый расчет в массив.
    """

    # data["result"] = 5
    # тут юзается функция вычисления и добавляется result в data
    # добавить логирование и обработчик ошибок

    redis_key = f"user_{current_user.id}"

    data_dict = is_existing_data(await redis.get(redis_key))

    request_key = f"request_{len(data_dict) + 1}"
    data_dict[request_key] = compute_construction.model_dump()

    await redis.set(redis_key, json.dumps(data_dict))

    logger.info(
        f"Добавлены данные для пользователя {redis_key} в Redis: {data_dict}."
    )

    return compute_construction


@router.post(
    '/create_compute_constructions',
    response_model=list[ComputeConstructionsCreate],
    response_model_exclude_none=True,
    dependencies=(Depends(current_user),)
)
@message_exception_handler(
    log_error_text=error_compute_message["constructions_log_error_text"],
    message_error_text=error_compute_message["constructions_message_error_text"]
)
async def compute_constructions(
    request: Request,
    compute_constructions: list[ComputeConstructionsCreate],
    current_user: User = Depends(current_user),
    redis: aioredis.Redis = Depends(get_redis_connection)
) -> list[ComputeConstructionsCreate]:
    """
    Только для пользователей.

    Получение и сохранение теплотехнических расчетов для нескольких
    элементов конструкций. Принимает список расчетов и сохраняет их в Redis.
    """

    # data["result"] = 5
    # тут юзается функция вычисления и добавляется result в data
    # добавить логирование и обработчик ошибок

    redis_key = f"user_{current_user.id}"

    data_dict = is_existing_data(await redis.get(redis_key))

    request_key = f"request_{len(data_dict) + 1}"
    data_dict[request_key] = [item.model_dump() for item in compute_constructions]

    await redis.set(redis_key, json.dumps(data_dict))

    logger.info(
        f"Добавлены данные для пользователя {redis_key} в Redis: {data_dict}."
    )

    return compute_constructions
