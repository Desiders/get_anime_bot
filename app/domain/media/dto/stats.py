from app.domain.common.dto import DTO


class Stats(DTO):
    total: int
    gif: int
    img: int
    all: int
    sfw: int
    nsfw: int
