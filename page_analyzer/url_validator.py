from urllib.parse import urlparse

import validators


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.hostname}"


def validate_url(url: str) -> dict[str, str]:
    errors: dict[str, str] = {}
    if url == "":
        errors["url"] = "URL не может быть пустым"
        return errors
    if len(url) > 255:
        errors["url"] = "Превышена максимальная длина URL (до 255 символов)"
        return errors
    if not validators.url(url):
        errors["url"] = "Некорректный URL"
    return errors
