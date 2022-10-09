from app.domain.common.dto import DTO


class Media(DTO):
    total: int
    genre: str
    media_type: str
    is_sfw: bool
