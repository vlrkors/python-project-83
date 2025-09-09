from bs4 import BeautifulSoup


def get_data(response):
    parsed = BeautifulSoup(response.text, "lxml")
    result: dict[str, str | None] = {}

    heading = parsed.h1.string if parsed.h1 else None
    title = parsed.title.string if parsed.title else None
    meta_desc = parsed.find("meta", {"name": "description"})

    result["h1"] = heading
    result["title"] = title
    result["description"] = meta_desc.get("content") if meta_desc else None

    return result
