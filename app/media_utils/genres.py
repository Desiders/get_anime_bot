from itertools import chain

from app.infrastructure.media import MediaSource
from app.typehints import I18nGettext


def get_sorted_genres_gif(
    sources: set[MediaSource],
    show_nsfw: bool,
) -> list[str]:
    if show_nsfw:
        genres = list(chain.from_iterable(source.genres_gif for source in sources))
    else:
        genres = list(chain.from_iterable(source.sfw_genres_gif for source in sources))
    return sorted(genres)


def get_sorted_genres_img(
    sources: set[MediaSource],
    show_nsfw: bool,
) -> list[str]:
    if show_nsfw:
        genres = list(chain.from_iterable(source.genres_img for source in sources))
    else:
        genres = list(chain.from_iterable(source.sfw_genres_img for source in sources))
    return sorted(genres)


def get_sorted_genres_all(
    sources: set[MediaSource],
    show_nsfw: bool,
) -> list[str]:
    if show_nsfw:
        genres = list(chain.from_iterable(source.genres_all for source in sources))
    else:
        genres = list(chain.from_iterable(source.sfw_genres_all for source in sources))
    return sorted(genres)


def get_sorted_genres(
    sources: set[MediaSource],
    show_nsfw: bool,
    genres_type: str,
) -> list[str]:
    if genres_type == "gif":
        return get_sorted_genres_gif(sources, show_nsfw)
    elif genres_type == "img":
        return get_sorted_genres_img(sources, show_nsfw)
    elif genres_type == "all":
        return get_sorted_genres_all(sources, show_nsfw)
    else:
        raise NotImplementedError(f"Unknown genres type `{genres_type}`")


def get_text_by_genres(genres: list[str], _: I18nGettext) -> str:
    if not genres:
        return _("No genres found")
    return _("Genres:\n\n{genres}").format(
        genres=" ".join(map(lambda string: "/" + string, genres)),
    )
