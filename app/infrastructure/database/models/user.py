from datetime import datetime

from app.infrastructure.database import Base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String


class UserModel(Base):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)

    language_code = Column(String, nullable=True)
    show_nsfw = Column(Boolean, default=False, nullable=False)

    created = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
