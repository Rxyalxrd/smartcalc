from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройка проекта.

    Взятие данных из .env и их валидация.
    """

    database_url: str
    redis_database_url: str
    app_title: str
    app_discription: str
    secret: str

    class Config:
        env_file = '.env'


settings = Settings()
