import json


def is_existing_data(
    data: bytes | None
) -> dict:
    """Проверка существования запросов у пользователя."""

    return json.loads(data) if data else {}
