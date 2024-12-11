import logging
from functools import wraps
from typing import Callable

from fastapi import HTTPException, Request, status

from app.utils.const.load_yaml_const import open_yaml
from app.loggers.log import setup_logging


setup_logging()
logger = logging.getLogger(__name__)

base_message_text = open_yaml("exception_const.yaml")


def message_exception_handler(
        log_error_text: str,
        message_error_text: str = base_message_text["base_message_error_text"]
) -> Callable:
    """Обработчик ошибок для FastAPI."""

    def decorator(endpoint: Callable):
        @wraps(endpoint)
        async def wrapper(request: Request, *args, **kwargs):
            try:
                return await endpoint(request, *args, **kwargs)
            except Exception as e:
                logger.error(f"{log_error_text}: {e}")

                return HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=message_error_text
                )

        return wrapper

    return decorator
