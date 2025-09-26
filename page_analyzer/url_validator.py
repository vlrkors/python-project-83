from urllib.parse import urlparse

import validators


def normalize_url(url: str) -> str:
    # Разбираем URL на компоненты
    parsed = urlparse(url)
    # Формируем нормализованный URL, используя схему и сетевое расположение
    # (включает учётные данные и порт, если они указаны)
    return f"{parsed.scheme}://{parsed.netloc}"


def validate_url(url: str) -> dict[str, str]:
    errors: dict[str, str] = {}
    # Проверяем, что URL не пустой
    if url == "":
        errors["url"] = "URL не может быть пустым"
        return errors
    # Проверяем максимальную длину URL
    if len(url) > 255:
        errors["url"] = "Превышена максимальная длина URL (до 255 символов)"
        return errors
    # Проверяем корректность URL с помощью валидатора
    if not validators.url(url):
        errors["url"] = "Некорректный URL"
    return errors
