from itertools import chain

from aiogram.dispatcher.filters import Filter
from aiogram.types import Message
from app.infrastructure.media.base.typehints import MediaGenreType


class CheckGenreIn(Filter):
    def __init__(self, genres: chain[MediaGenreType]):
        self.genres = set(genres)

    async def check(self, obj) -> bool:
        if not isinstance(obj, Message):
            return False

        return obj.get_command(pure=True) in self.genres
