from bs4 import BeautifulSoup


def get_data(response):
    parsed = BeautifulSoup(response.text, "lxml")
    result: dict[str, str | None] = {}

    heading = parsed.h1.get_text(strip=True) if parsed.h1 else None
    title = parsed.title.get_text(strip=True) if parsed.title else None
    meta_desc = parsed.find("meta", {"name": "description"})

    result["h1"] = heading
    result["title"] = title
    meta_content = meta_desc.get("content") if meta_desc else None
    result["description"] = meta_content.strip() if meta_content is not None else None

    return result
