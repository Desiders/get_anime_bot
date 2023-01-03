from datetime import datetime

from app.infrastructure.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)


class MediaModel(Base):  # type: ignore
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)

    url = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    media_type = Column(String, nullable=False)
    is_sfw = Column(Boolean, nullable=True)

    source_id = Column(
        Integer,
        ForeignKey(
            column="sources.id",
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
    )

    created = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    UniqueConstraint(url, genre, media_type)
