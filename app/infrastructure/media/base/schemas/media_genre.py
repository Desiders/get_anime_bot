from dataclasses import dataclass

from app.infrastructure.media.base.typehints import MediaRawGenreType


@dataclass(frozen=True)
class MediaGenre:
    raw_genre: MediaRawGenreType  # neko, foxgirl, etc.
    media_type: str  # gif, img, all
    is_sfw: bool
