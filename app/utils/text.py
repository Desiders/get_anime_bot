import collections
import typing
from pathlib import Path

import yaml


def get_all_texts_from_file(path: Path) -> typing.Dict[str, str]:
    with Path.open(
        path,
        mode="r",
        encoding="utf-8",
    ) as f:
        return yaml.load(f, yaml.SafeLoader)


def get_language(language_code: typing.Optional[str]) -> str:
    languages = collections.defaultdict(
        lambda: "en", dict(ru="ru")
    )

    if language_code is not None:
        return languages[language_code.split("-")[0]]
    return "en"


def get_path(filename: str) -> Path:
    return Path(__file__).parent.parent.joinpath(filename)


def get_text(
    language_code: typing.Optional[str],
    text_name: str,
) -> str:
    all_texts = get_all_texts_from_file(
        path=get_path(
            filename="texts.yaml"
        )
    )
    language = get_language(language_code=language_code)

    return all_texts[text_name][language]
