import collections
from pathlib import Path
from typing import Dict, Optional

import yaml


def get_all_texts_from_file(path: Path) -> Dict[str, str]:
    with Path.open(path, mode="r", encoding="utf-8") as file:
        texts = yaml.load(file, yaml.SafeLoader)
    return texts


def get_language(language_code: Optional[str]) -> str:
    languages = collections.defaultdict(
        lambda: "en", dict(ru="ru")
    )
    if language_code is not None:
        return languages[language_code.split("-")[0]]
    return "en"


def get_path(filename: str) -> Path:
    path = Path(__file__).parent.parent.joinpath(filename)
    return path


def get_text(language_code: Optional[str], text_name: str) -> str:
    all_texts = get_all_texts_from_file(
        path=get_path(
            filename="texts.yaml"
        )
    )
    language = get_language(language_code=language_code)
    text = all_texts[text_name][language]
    return text
