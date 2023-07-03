import sqlalchemy as sa

from file_uploader.enums import FileOwnerTypes

from .base import BaseTable

FILES_TABLE_NAME: str = 'attached_files'


class AttachedFile(BaseTable):
    __tablename__ = FILES_TABLE_NAME

    filename = sa.Column(
        sa.Text,
        doc='Имя загруженного файла',
    )

    size = sa.Column(
        sa.Integer,
        doc='Размер загруженного файла',
    )

    owner_id = sa.Column(
        sa.Integer,
    )

    owner_type = sa.Column(
        sa.Enum(FileOwnerTypes)
    )

    content_type = sa.Column(
        sa.Text,
        doc='Тип загруженного файла',
    )

    __table_args__ = (
        sa.UniqueConstraint("filename", "owner_id", "owner_type", "content_type", name="table_fields_uc"),
    )
