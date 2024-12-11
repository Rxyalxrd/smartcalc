import os

import yaml


def open_yaml(filename: str) -> dict[str, str]:
    """Открывает YAML файл с указанной кодировкой UTF-8."""

    if not os.path.exists(f"app/utils/const/{filename}"):
        raise FileNotFoundError(f"Файл {filename} не найден.")

    with open(f"app/utils/const/{filename}", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
