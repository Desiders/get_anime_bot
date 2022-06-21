from abc import ABC, abstractmethod
from typing import Optional

from aiohttp import ClientSession, ClientTimeout
from app.infrastructure.media.base.schemas import Media, MediaGenre
from app.infrastructure.media.base.typehints import MediaGenreType


class MediaSource(ABC):
    SOURCE_URL: str
    SOURCE_ID: str

    RAW_SFW_GENRES: dict[str, set[str]]
    RAW_NSFW_GENRES: dict[str, set[str]]

    def __init__(self):
        self._session: Optional[ClientSession] = None

    @abstractmethod
    async def get_media(
        self,
        genre: MediaGenreType,
        count: int = 1,
    ) -> list[Media]:
        """
        Get media for the given genre.

        :genre: genre to get media for
        :count (optional): number of media to get
        """
        ...

    @property
    def session(self) -> ClientSession:
        """
        Get a session for the nekos.life API.
        """
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                timeout=ClientTimeout(total=30),
            )
        return self._session

    async def close(self) -> None:
        """
        Close the session.
        """
        if self._session is not None and not self._session.closed:
            await self._session.close()

    @property
    def sfw_genres(self) -> set[MediaGenreType]:
        """
        Genres that are safe for work.
        """
        source_id = self.SOURCE_ID

        return {
            # key=gif, genre=neko => neko_gif__SOURCE_ID
            # key=img, genre=neko => neko_img__SOURCE_ID
            # key=all, genre=neko => neko_all__SOURCE_ID
            f"{genre}_{key}__{source_id}"
            for key, genres in self.RAW_SFW_GENRES.items()
            for genre in genres
        }

    @property
    def sfw_genres_gif(self) -> set[MediaGenreType]:
        """
        Genres that are safe for work and are gifs.
        """
        source_id = self.SOURCE_ID

        return {
            # key=gif, genre=neko => neko_gif__SOURCE_ID
            f"{genre}_gif__{source_id}"
            for genre in self.RAW_SFW_GENRES["gif"]
        }

    @property
    def sfw_genres_img(self) -> set[MediaGenreType]:
        """
        Genres that are safe for work and are images.
        """
        source_id = self.SOURCE_ID

        return {
            # key=img, genre=neko => neko_img__SOURCE_ID
            f"{genre}_img__{source_id}"
            for genre in self.RAW_SFW_GENRES["img"]
        }

    @property
    def sfw_genres_all(self) -> set[MediaGenreType]:
        """
        Genres that are safe for work and are gifs and images.
        """
        source_id = self.SOURCE_ID

        return {
            # key=all, genre=neko => neko_all__SOURCE_ID
            f"{genre}_all__{source_id}"
            for genre in self.RAW_SFW_GENRES["all"]
        }

    @property
    def nsfw_genres(self) -> set[MediaGenreType]:
        """
        Genres that are not safe for work.
        """
        source_id = self.SOURCE_ID

        return {
            # key=gif, genre=neko => neko_gif_nsfw__SOURCE_ID
            # key=img, genre=neko => neko_img_nsfw__SOURCE_ID
            # key=all, genre=neko => neko_all_nsfw__SOURCE_ID
            f"{genre}_{key}_nsfw__{source_id}"
            for key, genres in self.RAW_NSFW_GENRES.items()
            for genre in genres
        }

    @property
    def nsfw_genres_gif(self) -> set[MediaGenreType]:
        """
        Genres that are not safe for work and are gifs.
        """
        source_id = self.SOURCE_ID

        return {
            # key=gif, genre=neko => neko_gif_nsfw__SOURCE_ID
            f"{genre}_gif_nsfw__{source_id}"
            for genre in self.RAW_NSFW_GENRES["gif"]
        }

    @property
    def nsfw_genres_img(self) -> set[MediaGenreType]:
        """
        Genres that are not safe for work and are images.
        """
        source_id = self.SOURCE_ID

        return {
            # key=img, genre=neko => neko_img_nsfw__SOURCE_ID
            f"{genre}_img_nsfw__{source_id}"
            for genre in self.RAW_NSFW_GENRES["img"]
        }

    @property
    def nsfw_genres_all(self) -> set[MediaGenreType]:
        """
        Genres that are not safe for work and are gifs and images.
        """
        source_id = self.SOURCE_ID

        return {
            # key=all, genre=neko => neko_all_nsfw__SOURCE_ID
            f"{genre}_all_nsfw__{source_id}"
            for genre in self.RAW_NSFW_GENRES["all"]
        }

    @property
    def genres(self) -> set[MediaGenreType]:
        """
        All genres.
        """
        return self.sfw_genres | self.nsfw_genres

    @property
    def genres_gif(self) -> set[MediaGenreType]:
        """
        All gif genres.
        """
        return self.sfw_genres_gif | self.nsfw_genres_gif

    @property
    def genres_img(self) -> set[MediaGenreType]:
        """
        All image genres.
        """
        return self.sfw_genres_img | self.nsfw_genres_img

    @property
    def genres_all(self) -> set[MediaGenreType]:
        """
        All gif and image genres.
        """
        return self.sfw_genres_all | self.nsfw_genres_all

    def parse_genre(self, genre: MediaGenreType) -> MediaGenre:
        """
        Parse a genre into a `MediaGenre`.

        :genre: genre to parse
        """
        raw_genre, media_type, *args = genre.rsplit("_")
        is_nsfw = args[0] == "nsfw"

        if is_nsfw:
            return MediaGenre(
                raw_genre=raw_genre,
                media_type=media_type,
                is_sfw=False,
            )
        return MediaGenre(
            raw_genre=raw_genre,
            media_type=media_type,
            is_sfw=True,
        )
