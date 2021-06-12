import uuid

from sqlalchemy import Column

from sqlalchemy_utils import UUIDType

from app.infra.orm import Base


class Sample(Base):
    id = Column(
        UUIDType,
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
        comment='ID'
    )

    __tablename__ = 'sample'
