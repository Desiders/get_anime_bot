from datetime import datetime

from app.infrastructure.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer


class ViewModel(Base):
    __tablename__ = "views"

    id = Column(Integer, primary_key=True)

    user_tg_id = Column(
        Integer,
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
