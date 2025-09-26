from bs4 import BeautifulSoup


def get_data(response):
    # Парсим HTML-ответ с помощью BeautifulSoup и парсера lxml
    parsed = BeautifulSoup(response.text, "lxml")
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

    # Возвращаем словарь с полученными данными
    return result
