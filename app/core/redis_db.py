import redis.asyncio as aioredis
from app.core.config import settings


async def get_redis_connection() -> aioredis.Redis:
    """Подключение к Redis."""

    return await aioredis.from_url(
        settings.redis_database_url, decode_responses=True
    )
