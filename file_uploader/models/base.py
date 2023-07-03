import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func

from file_uploader.db import DeclarativeBase


class BaseTable(DeclarativeBase):
    __abstract__ = True

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        doc="Unique index of element",
    )

    dt_created = sa.Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
        doc="Date and time of create (type TIMESTAMP)",
    )

    dt_updated = sa.Column(
        TIMESTAMP(timezone=True),
        nullable=True,
        doc="Date and time of update (type TIMESTAMP)",
    )

    is_available = sa.Column(
        sa.Boolean,
        nullable=False,
        default=True,
    )

    def __repr__(self):
        sa.Columns = {sa.Column.name: getattr(self, sa.Column.name) for sa.Column in self.__table__.sa.Columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", sa.Columns.items()))}>'
