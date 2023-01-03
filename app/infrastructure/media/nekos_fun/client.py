from app.infrastructure.media.base import MediaSource
from app.infrastructure.media.base.exceptions import GenreNotFound
from app.infrastructure.media.base.schemas import Media, MediaGenre
from app.infrastructure.media.base.typehints import MediaGenreType
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


class NekosFun(MediaSource):
    SOURCE_URL = "http://api.nekos.fun:8080/api"
    SOURCE_ID = "nf"

    RAW_SFW_GENRES: dict[str, set[str]] = {
        "gif": {
            "kiss",
            "lick",
            "hug",
            "baka",
            "cry",
            "poke",
            "smug",
            "slap",
            "tickle",
            "pat",
            "laugh",
            "feed",
            "cuddle",
        },
        "img": {
            "animalears",
            "foxgirl",
            "neko",
        },
        "all": set(),
    }
    RAW_NSFW_GENRES: dict[str, set[str]] = {
        "gif": {
            "boobs",
            "cum",
            "lesbian",
            "anal",
        },
        "img": {
            "hentai",
            "lewd",
            "holo",
        },
        "all": {
            "blowjob",
            "spank",
            "pussy",
            "feet",
        },
    }

    async def get_media(
        self,
        genre: MediaGenreType,
        count: int = 1,
    ) -> list[Media]:
        """
        Get a media url for a given genre.

        :genre: genre to get a media url for
        :count (optional): number of media to get
        """
        if genre not in self.genres:
            raise GenreNotFound

        genre_model = self.parse_genre(genre)

        url = self.generate_url(genre_model)

        if count > 1:
            media = []

            for _ in range(count):
                response = await self.session.get(url=url)
                response.raise_for_status()

                result = await response.json()

                media.append(
                    Media(
                        url=result["image"],
                        media_type=genre_model.media_type,
                        is_sfw=genre_model.is_sfw,
                        raw_genre=genre_model.raw_genre,
                    )
                )
            return media

        response = await self.session.get(url=url)
        response.raise_for_status()

        result = await response.json()

        return [
            Media(
                url=result["image"],
                media_type=genre_model.media_type,
                is_sfw=genre_model.is_sfw,
                raw_genre=genre_model.raw_genre,
            )
        ]

    def generate_url(self, genre_model: MediaGenre) -> MediaGenreType:
        """
        Generate a url for a given genre model.

        :genre_model: genre model to generate a url for
        """
        url = "{source_url}/{raw_genre}".format(
            source_url=self.SOURCE_URL,
            raw_genre=genre_model.raw_genre,
        )

        return url
