from app.typehints import I18nGettext


def get_text(genres: list[str], _: I18nGettext) -> str:
    if not genres:
        return _("No genres found")
    return _(
        "Genres:\n\n{genres}"
    ).format(
        genres=" ".join(map(lambda string: "/" + string, genres)),
    )
