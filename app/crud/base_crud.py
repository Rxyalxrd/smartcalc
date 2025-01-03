from dataclasses import dataclass
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from app.models.user import User


@dataclass
class CRUD:
    """Реализация работы с БД: Create, Read, ReadAll, Update, Delete."""

    model: User

    async def create(
        self,
        request: BaseModel,
        session: AsyncSession,
        user: User | None = None
    ):
        """Создание новой записи в БД."""

        data_in_request = request.model_dump()

        if user is not None:
            data_in_request['user_id'] = user.id

        data_to_db = self.model(**data_in_request)

        session.add(data_to_db)
        await session.commit()
        await session.refresh(data_to_db)

        return data_to_db

    async def read(
        self,
        record_id: int,
        session: AsyncSession
    ):
        """Чтение записи из БД по ID."""

        return await session.get(self.model, record_id)

    async def read_all(
        self,
        session: AsyncSession
    ):
        """Чтение всех записей из БД."""

        all_records = await session.execute(select(self.model))

        return all_records.scalars().all()

    async def update(
        self,
        db_record,
        request: BaseModel,
        session: AsyncSession
    ):
        """Обновление записи в БД."""

        db_record_data = jsonable_encoder(db_record)
        update_data = request.model_dump(exclude_unset=True)

        for field in db_record_data:
            if field in update_data:
                setattr(db_record, field, update_data[field])

        session.add(db_record)
        await session.commit()
        await session.refresh(db_record)

        return db_record

    async def delete(
        self,
        model_in_db,
        session: AsyncSession
    ):
        """Удаление записи из БД."""

        await session.delete(model_in_db)
        await session.commit()

        return model_in_db
