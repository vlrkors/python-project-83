from typing import Any

from bs4 import BeautifulSoup

_DEFAULT_ENCODING = "utf-8"


def _coerce_to_text(source: Any, encoding: str) -> str:
    """Возвращает HTML как строку, декодируя байты при необходимости."""

    if isinstance(source, str):
        return source
    if isinstance(source, bytes):
        return source.decode(encoding, errors="strict")

    content = getattr(source, "content", None)
    if content is not None:
        return _coerce_to_text(content, encoding)

    text = getattr(source, "text", None)
    if text is not None:
        return text

    msg = "Unsupported HTML source. Provide str, bytes, or response-like object."
    raise TypeError(msg)


def get_data(response: Any) -> dict[str, str | None]:
    """Извлекает базовые SEO-данные из HTML-ответа."""

    encoding = getattr(response, "encoding", None) or _DEFAULT_ENCODING
    html = _coerce_to_text(response, encoding)

    parsed = BeautifulSoup(html, "lxml")
    result: dict[str, str | None] = {}

    # Извлекаем текст из первого тега h1, если он есть
    heading = parsed.h1.get_text(strip=True) if parsed.h1 else None
    # Извлекаем текст из тега title, если он есть
    title = parsed.title.get_text(strip=True) if parsed.title else None
    # Находим тег meta с атрибутом name="description"
    meta_desc = parsed.find("meta", {"name": "description"})

    result["h1"] = heading
    result["title"] = title
    # Получаем содержимое атрибута content из meta description, если он существует
    meta_content = meta_desc.get("content") if meta_desc else None
    # Удаляем лишние пробелы и сохраняем описание в результат
    result["description"] = meta_content.strip() if meta_content is not None else None

    return result
