from operator import attrgetter

from app.domain.media.dto import Media, Stats
from app.typehints import I18nGettext


def get_sorted_media_by_total(media: list[Media]) -> list[Media]:
    return sorted(media, key=attrgetter("total"), reverse=True)


def get_media_stats_text(media: list[Media], _: I18nGettext) -> str:
    if media := get_sorted_media_by_total(media):
        text = "\n\t- ".join([
            "{genre}: {total}".format(
                genre=media.genre, total=media.total,
            )
            for media in get_sorted_media_by_total(media)
        ])
    else:
        text = _("No media found")
    return "\t- " + text


def get_media_gif_stats_text(
    media: list[Media], is_sfw: bool, _: I18nGettext
) -> str:
    return get_media_stats_text(
        [
            media
            for media in media
            if (
                media.media_type == "gif" and
                media.is_sfw == is_sfw
            )
        ], _,
    )


def get_media_img_stats_text(
    media: list[Media], is_sfw: bool,  _: I18nGettext
) -> str:
    return get_media_stats_text(
        [
            media
            for media in media
            if (
                media.media_type == "img" and
                media.is_sfw == is_sfw
            )
        ], _,
    )


def get_media_all_stats_text(
    media: list[Media], is_sfw: bool, _: I18nGettext
) -> str:
    return get_media_stats_text(
        [
            media
            for media in media
            if media.is_sfw == is_sfw
        ], _,
    )


def get_stats_text(stats: Stats, _: I18nGettext) -> str:
    media = stats.media

    sfw_media_gif = get_media_gif_stats_text(media, True, _)
    nsfw_media_gif = get_media_gif_stats_text(media, False, _)
    sfw_media_img = get_media_img_stats_text(media, True, _)
    nsfw_media_img = get_media_img_stats_text(media, False, _)
    sfw_media_all = get_media_all_stats_text(media, True, _)
    nsfw_media_all = get_media_all_stats_text(media, False, _)

    return _(
        "Total count: {total}\n"
        "GIF count: {gif}\n"
        "\tGenres SFW count:\n"
        "{sfw_media_gif_stats_text}\n"
        "\tGenres NSFW count:\n"
        "{nsfw_media_gif_stats_text}\n"
        "IMG count: {img}\n"
        "\tGenres SFW count:\n"
        "{sfw_media_img_stats_text}\n"
        "\tGenres NSFW count:\n"
        "{nsfw_media_img_stats_text}\n"
        "ALL count: {all}\n"
        "\tGenres SFW count:\n"
        "{sfw_media_all_stats_text}\n"
        "\tGenres NSFW count:\n"
        "{nsfw_media_all_stats_text}\n"
        "SFW count: {sfw}\n"
        "NSFW count: {nsfw}"
    ).format(
        total=stats.total,
        gif=stats.gif,
        img=stats.img,
        all=stats.all,
        sfw=stats.sfw,
        nsfw=stats.nsfw,
        sfw_media_gif_stats_text=sfw_media_gif,
        nsfw_media_gif_stats_text=nsfw_media_gif,
        sfw_media_img_stats_text=sfw_media_img,
        nsfw_media_img_stats_text=nsfw_media_img,
        sfw_media_all_stats_text=sfw_media_all,
        nsfw_media_all_stats_text=nsfw_media_all,
    )
