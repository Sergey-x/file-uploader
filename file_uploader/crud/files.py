import fastapi as fa
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from file_uploader.enums import FileOwnerTypes
from file_uploader.models import AttachedFile


class FilesCRUD:
    @classmethod
    async def insert_file(
            cls,
            db: AsyncSession,
            file: fa.File,
            owner_id: int,
            owner_type: FileOwnerTypes,
    ) -> int | None:
        new_value_dict: dict = dict(owner_type=owner_type,
                                    owner_id=owner_id,
                                    filename=file.filename,
                                    content_type=file.content_type,
                                    size=123,
                                    is_available=True,
                                    )

        insert_stmt = insert(AttachedFile).values(owner_type=owner_type,
                                                  owner_id=owner_id,
                                                  filename=file.filename,
                                                  content_type=file.content_type,
                                                  size=file.size, )

        do_update_stmt = insert_stmt.on_conflict_do_update(constraint="table_fields_uc",
                                                           set_=new_value_dict).returning(AttachedFile.id)

        try:
            res = await db.execute(do_update_stmt)
            return res.one()[0]
        except sa.exc.OperationalError:
            return None

    @classmethod
    async def get_event_files(
            cls,
            db: AsyncSession,
            owner_id: int,
            owner_type: FileOwnerTypes,
    ):
        stmt = sa.select(AttachedFile).where(AttachedFile.owner_id == owner_id,
                                             AttachedFile.owner_type == owner_type,
                                             AttachedFile.is_available == True)  # noqa
        return (await db.scalars(stmt)).all()

    @classmethod
    async def get_event_file(
            cls,
            db: AsyncSession,
            file_id: int,
    ):
        """Получить файл по его уникальному идентификатору."""
        stmt = sa.select(AttachedFile).where(AttachedFile.id == file_id, AttachedFile.is_available == True)  # noqa
        try:
            return (await db.scalars(stmt)).one()
        except NoResultFound:
            return None

    @classmethod
    async def get_events_files(
            cls,
            db: AsyncSession,
            owner_type: FileOwnerTypes,
            owner_ids: list[int],
    ) -> list:
        """Получить файлы событий типа `owner_type` с идентификаторами в `owner_ids`."""
        criteria = sa.and_(AttachedFile.owner_type == owner_type, AttachedFile.is_available == True)  # noqa
        # Если идентификаторы не заданы - вытаскиваем все
        if len(owner_ids) != 0:
            # Если идентификаторы заданы - вытаскиваем только то, что надо
            criteria = sa.and_(criteria, AttachedFile.owner_id.in_(owner_ids))

        stmt = sa.select(AttachedFile).where(criteria)
        try:
            return (await db.scalars(stmt)).all()
        except NoResultFound:
            return []

    @classmethod
    async def delete_event_file(cls, db: AsyncSession, file_id: int):
        stmt = sa.update(AttachedFile).where(AttachedFile.id == file_id).values(
            is_available=False)
        await db.execute(stmt)
        await db.commit()

    @classmethod
    async def delete_event_files(cls, db: AsyncSession, owner_type: FileOwnerTypes, owner_id: int):
        # Удаление файла фиксируется в вызывающем коде!
        stmt = sa.update(AttachedFile) \
            .where(AttachedFile.owner_id == owner_id, AttachedFile.owner_type == owner_type) \
            .values(is_available=False)
        return await db.execute(stmt)
