from datetime import datetime

from app.infrastructure.database import Base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)

    language_code = Column(String, nullable=True)
    show_nsfw = Column(Boolean, default=False, nullable=False)

    # TODO: add views media for user
    views = relationship(
        "ViewModel",
        cascade="all, delete-orphan",
        uselist=False,
    )

    created = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
