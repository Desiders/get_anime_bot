from dataclasses import dataclass


@dataclass(frozen=True)
class Media:
    url: str
    media_type: str  # gif, jpg, jpeg, png
    is_sfw: bool
    raw_genre: str  # hentai, neko, etc.
