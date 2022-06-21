from app.infrastructure.media.base import MediaSource
from app.infrastructure.media.base.exceptions import GenreNotFound
from app.infrastructure.media.base.schemas import Media, MediaGenre
from app.infrastructure.media.base.typehints import (MediaGenreType,
                                                     MediaUrlType)
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


class WaifuPics(MediaSource):
    SOURCE_URL = "https://api.waifu.pics"
    SOURCE_ID = "wp"

    RAW_SFW_GENRES: dict[str, set[str]] = {
        "gif": {
            "bully", "cuddle", "cry",
            "hug", "kiss", "lick",
            "pat", "smug", "bonk",
            "yeet", "blush", "smile",
            "wave", "nom", "bite",
            "glomp", "slap", "kill",
            "kick", "happy", "wink",
            "poke", "dance", "cringe",
        },
        "img": {
            "waifu", "neko", "shinobu",
            "megumin", "awoo",
        },
        "all": set(),
    }
    RAW_NSFW_GENRES: dict[str, set[str]] = {
        "gif": {
            "blowjob",
        },
        "img": {
            "waifu", "neko", "trap",
        },
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
        :count (optional): number of media to get. 1 <= count <= 30
        """
        if genre not in self.genres:
            raise GenreNotFound

        genre_model = self.parse_genre(genre)

        many = count > 1

        if genre_model.is_sfw:
            url = self.generate_sfw_url(genre_model, many)
        else:
            url = self.generate_nsfw_url(genre_model, many)

        response = await self.session.get(url=url)
        response.raise_for_status()

        result = await response.json()

        logger.info("Got result", result=result)

        if many:
            return [
                Media(
                    url=url,
                    media_type=genre_model.media_type,
                    is_sfw=genre_model.is_sfw,
                    raw_genre=genre_model.raw_genre,
                )
                for url in result["files"][:many]
            ]
        else:
            return [
                Media(
                    url=result["url"],
                    media_type=genre_model.media_type,
                    is_sfw=genre_model.is_sfw,
                    raw_genre=genre_model.raw_genre,
                )
            ]

    def generate_sfw_url(
        self,
        genre_model: MediaGenre,
        many: bool = False,
    ) -> MediaUrlType:
        """
        Generate a sfw url for a given genre model.

        :genre_model: genre model to generate a url for
        :many: whether to generate a url for multiple media
        """
        if many:
            url = "{source_url}/many/sfw/{raw_genre}".format(
                source_url=self.SOURCE_URL,
                raw_genre=genre_model.raw_genre,
            )
        else:
            url = "{source_url}/sfw/{raw_genre}".format(
                source_url=self.SOURCE_URL,
                raw_genre=genre_model.raw_genre,
            )

        return url

    def generate_nsfw_url(
        self,
        genre_model: MediaGenre,
        many: bool = False,
    ) -> MediaUrlType:
        """
        Generate a nsfw url for a given genre model.

        :genre_model: genre model to generate a url for
        :many: whether to generate a url for multiple media
        """
        if many:
            url = "{source_url}/many/nsfw/{raw_genre}".format(
                source_url=self.SOURCE_URL,
                raw_genre=genre_model.raw_genre,
            )
        else:
            url = "{source_url}/nsfw/{raw_genre}".format(
                source_url=self.SOURCE_URL,
                raw_genre=genre_model.raw_genre,
            )

        return url
