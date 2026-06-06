import json
from pathlib import Path
from typing import Dict

TRANS_DIR = Path(__file__).resolve().parent / "translations"
_cache: Dict[str, Dict[str, str]] = {}


def load_translations(lang: str) -> Dict[str, str]:
    if lang not in _cache:
        path = TRANS_DIR / f"{lang}.json"
        if path.exists():
            with open(path, encoding="utf-8") as f:
                _cache[lang] = json.load(f)
        else:
            _cache[lang] = {}
    return _cache[lang]


class Translator:
    def __init__(self, lang: str):
        self.lang = lang if lang in ("en", "fr") else "en"
        self.translations = load_translations(self.lang)

    def t(self, key: str, default: str = "") -> str:
        return self.translations.get(key, default or key)

    def __call__(self, key: str, default: str = "") -> str:
        return self.t(key, default)


AVAILABLE_LANGUAGES = {
    "en": "English",
    "fr": "Français",
}
