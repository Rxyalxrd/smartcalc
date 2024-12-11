import logging
from pathlib import Path

log_dir = Path(__file__).parent / "log_levels"
log_dir.mkdir(exist_ok=True)


class LevelFilter(logging.Filter):
    """Фильтрация логов определенного уровня."""

    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


def create_file_handler(level: int, log_file: Path) -> logging.FileHandler:
    """Создание файла с логами."""

    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setLevel(level)
    handler.addFilter(LevelFilter(level))
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))
    return handler


def setup_logging():
    """Настройка логов."""

    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    log_files = {
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "debug": logging.DEBUG,
    }

    for name, level in log_files.items():
        logger.addHandler(create_file_handler(level, log_dir / f"{name}.log"))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(console_handler)

    alembic_logger = logging.getLogger("alembic")
    alembic_logger.setLevel(logging.INFO)

    alembic_files = {
        "alembic_info": logging.INFO,
        "alembic_error": logging.ERROR,
    }

    for name, level in alembic_files.items():
        alembic_logger.addHandler(create_file_handler(
            level, log_dir / f"{name}.log"
        ))
