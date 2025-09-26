import types

import pytest

from page_analyzer.parser import get_data


@pytest.mark.parametrize(
    "html, expected",
    [
        pytest.param(
            """
            <html><head><title>Sample Title</title>
            <meta name='description' content='Short description'></head>
            <body><h1>Heading</h1></body></html>
            """,
            {"h1": "Heading", "title": "Sample Title", "description": "Short description"},
            id="basic-elements",
        ),
        pytest.param(
            """
            <html><head><title>  Nested   Title  </title></head>
            <body><h1><span>Nested</span><em>Heading</em></h1></body></html>
            """,
            {"h1": "NestedHeading", "title": "Nested   Title", "description": None},
            id="nested-tags",
        ),
        pytest.param(
            """
            <html><head><meta name='description' content='   With surrounding spaces   '></head>
            <body></body></html>
            """,
            {"h1": None, "title": None, "description": "With surrounding spaces"},
            id="description-strip",
        ),
        pytest.param(
            """
            <html><head><title></title><meta name='description' content=''></head><body></body></html>
            """,
            {"h1": None, "title": "", "description": ""},
            id="empty-values",
        ),
        pytest.param(
            """
            <html><head><title>{title}</title><meta name='description' content='{description}'></head>
            <body><h1>{heading}</h1></body></html>
            """.format(
                title="T" * 300,
                description="D" * 512,
                heading="H" * 256,
            ),
            {
                "h1": "H" * 256,
                "title": "T" * 300,
                "description": "D" * 512,
            },
            id="long-values",
        ),
    ],
)
def test_get_data_returns_expected(html, expected):
    response = types.SimpleNamespace(text=html)

    result = get_data(response)

    assert result == expected
