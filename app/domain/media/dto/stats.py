from app.domain.common.dto import DTO

from .media import Media


class Stats(DTO):
    total: int
    gif: int
    img: int
    all: int
    sfw: int
    nsfw: int
    media: list[Media]
