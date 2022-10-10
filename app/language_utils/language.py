from dataclasses import dataclass, field


@dataclass
class LanguageData:
    code: str
    flag: str
    title: str
    label: str | None = field(init=False, default=None)

    def __post_init__(self):
        self.label = f"{self.flag} {self.title}"


AVAILABLE_LANGUAGES = {
    "en": LanguageData(
        code="en",
        flag="🇺🇸",
        title="English",
    ),
    "ru": LanguageData(
        code="ru",
        flag="🇷🇺",
        title="Русский",
    ),
    "ua": LanguageData(
        code="ua",
        flag="🇺🇦",
        title="Українська",
    ),
    "be": LanguageData(
        code="be",
        flag="🇧🇾",
        title="Беларуская",
    ),
}
DEFAULT_LANGUAGE = AVAILABLE_LANGUAGES["en"]


def get_locale_or_default(locale: str | None = None) -> str:
    if not locale:
        return DEFAULT_LANGUAGE.code

    if locale not in AVAILABLE_LANGUAGES:
        return DEFAULT_LANGUAGE.code

    return locale
