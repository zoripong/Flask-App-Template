import uuid

from sqlalchemy import Column, String

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

    name = Column(String, nullable=False, comment='이름')

    __tablename__ = 'sample'
