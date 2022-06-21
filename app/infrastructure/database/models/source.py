from datetime import datetime

from app.infrastructure.database import Base
from sqlalchemy import Column, DateTime, Integer, String


class SourceModel(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False, unique=True)

    created = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
