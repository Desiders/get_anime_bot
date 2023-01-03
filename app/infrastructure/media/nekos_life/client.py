from app.infrastructure.media.base import MediaSource
from app.infrastructure.media.base.exceptions import GenreNotFound
from app.infrastructure.media.base.schemas import Media, MediaGenre
from app.infrastructure.media.base.typehints import MediaGenreType, MediaUrlType
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


class NekosLife(MediaSource):
    SOURCE_URL = "https://api.nekos.dev/api/v3/images"
    SOURCE_ID = "nl"

    RAW_SFW_GENRES: dict[str, set[str]] = {
        "gif": {
            "tickle",
            "poke",
            "kiss",
            "slap",
            "cuddle",
            "hug",
            "pat",
            "feed",
            "neko",
            "smug",
            "baka",
        },
        "img": {
            "neko",
            "kitsune",
            "holo",
            "wallpaper",
        },
        "all": set(),
    }
    RAW_NSFW_GENRES: dict[str, set[str]] = {
        "gif": set(),
        "img": set(),
        "all": set(),
    }

    async def get_media(
        self,
        genre: MediaGenreType,
        count: int = 1,
    ) -> list[Media]:
        """
        Get a media url for a given genre.

        :genre: genre to get a media url for
        :count (optional): number of media to get. 1 <= count <= 20
        """
        if genre not in self.genres:
            raise GenreNotFound

        if count == 1:
            # the source handling the error by 1.
            # 0 is good, but `count=0` is 1 url and `count=2` is 2 urls ^_^
            count = 0

        genre_model = self.parse_genre(genre)

        if genre_model.is_sfw:
            url = self.generate_sfw_url(genre_model)
        else:
            url = self.generate_nsfw_url(genre_model)

        response = await self.session.get(url=url, params={"count": count})
        response.raise_for_status()

        result = await response.json()

        if url := result["data"]["response"].get("url"):
            return [
                Media(
                    url=url,
                    media_type=genre_model.media_type,
                    is_sfw=genre_model.is_sfw,
                    raw_genre=genre_model.raw_genre,
                )
            ]
        return [
            Media(
                url=url,
                media_type=genre_model.media_type,
                is_sfw=genre_model.is_sfw,
                raw_genre=genre_model.raw_genre,
            )
            for url in result["data"]["response"]["urls"]
        ]

    def generate_sfw_url(self, genre_model: MediaGenre) -> MediaUrlType:
        """
        Generate a sfw url for a given genre model.

        :genre_model: genre model to generate a url for
        """
        url = "{source_url}/sfw/{media_type}/{raw_genre}".format(
            source_url=self.SOURCE_URL,
            media_type=genre_model.media_type,
            raw_genre=genre_model.raw_genre,
        )

        return url

    def generate_nsfw_url(self, genre_model: MediaGenre) -> MediaUrlType:
        """
        Generate a nsfw url for a given genre model.

        :genre_model: genre model to generate a url for
        """
        url = "{source_url}/nsfw/{media_type}/{raw_genre}".format(
            source_url=self.SOURCE_URL,
            media_type=genre_model.media_type,
            raw_genre=genre_model.raw_genre,
        )

        return url
