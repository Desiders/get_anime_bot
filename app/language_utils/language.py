from dataclasses import dataclass, field


@dataclass
class LanguageData:
    code: str
    flag: str
    title: str
    label: str | None = field(init=False, default=None)

    def __post_init__(self):
        self.label = f"{self.flag} {self.title}"


DEFAULT_LANGUAGE = LanguageData(
    code="en",
    flag="🇺🇸",
    title="English",
)
AVAILABLE_LANGUAGES = {
    "en": DEFAULT_LANGUAGE,
    "ru": LanguageData(
        code="ru",
        flag="🇷🇺",
        title="Русский",
    ),
}


def get_locale_or_default(locale: str | None = None) -> str:
    if not locale:
        return DEFAULT_LANGUAGE.code

    if locale not in AVAILABLE_LANGUAGES:
        return DEFAULT_LANGUAGE.code

    return locale
