from urllib.parse import urlparse, urlunparse

import validators


def normalize_url(url: str) -> str:
    # Разбираем URL на компоненты
    parsed = urlparse(url)
    # Приводим схему к нижнему регистру
    scheme = parsed.scheme.lower()

    # Сохраняем пользовательскую часть, если она присутствует
    userinfo = ""
    host_port = parsed.netloc
    if "@" in host_port:
        # Разделяем userinfo и хост с портом
        userinfo, host_port = host_port.rsplit("@", 1)
        userinfo = f"{userinfo}@"

    # Разделяем хост и порт, учитывая IPv6-адреса в квадратных скобках
    host = host_port
    port = ""
    if host_port.startswith("["):
        # Если адрес IPv6, ищем закрывающую скобку
        closing = host_port.find("]")
        if closing != -1:
            # Отделяем хост и порт после IPv6-адреса
            host = host_port[: closing + 1]
            port = host_port[closing + 1 :]
        else:
            # Если закрывающей скобки нет, берем весь netloc как хост
            host = host_port
            port = ""
    elif ":" in host_port:
        # Если обычный хост с портом, разделяем их
        host, port_value = host_port.split(":", 1)
        port = f":{port_value}"

    # Приводим хост к нижнему регистру, сохраняя порт и учётные данные
    netloc = f"{userinfo}{host.lower()}{port}"

    # Собираем нормализованный URL, оставляя только схему и
    # сетевое расположение
    normalized = parsed._replace(
        scheme=scheme,
        netloc=netloc,
        path="",  # Убираем путь
        params="",  # Убираем параметры
        query="",  # Убираем строку запроса
        fragment="",  # Убираем фрагмент
    )
    return urlunparse(normalized)


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
