from datetime import datetime

from app.infrastructure.database import Base
from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Integer,
                        UniqueConstraint)


class ViewModel(Base):
    __tablename__ = "views"

    id = Column(Integer, primary_key=True)

    user_tg_id = Column(
        BigInteger,
        ForeignKey(
            column="users.tg_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    media_id = Column(
        Integer,
        ForeignKey(
            column="media.id",
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
    )

    created = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    UniqueConstraint(user_tg_id, media_id)
