PACKAGE = ""
MSG = ""

# Устанавливает зависимости, указанные в pyproject.toml
install:
	poetry install --no-root

# Добавляет новый пакет в проект
# Использование: make install-package PACKAGE=<имя_пакета>
install-package:
	poetry add $(PACKAGE)

# Обновляет все зависимости до последних версий
update:
	poetry update

# Очищает файлы .pyc, которые создаются при компиляции Python
clean:
	find . -name "*.pyc" -delete

# Форматирует код по стандарту black
format:
	poetry run black .

# Запуск приложения
run:
	uvicorn app.main:app --reload

# Применяет последние миграции к базе данных
migrate:
	poetry run alembic upgrade head

# Откатывает последнюю миграцию базы данных
downgrade:
	poetry run alembic downgrade -1 

# Создает новую миграцию на основе изменений в моделях
# Использование: make makemigration msg="описание изменений"
makemigration:
	poetry run alembic revision --autogenerate -m "$(MSG)"
