import pytest
from bs4 import BeautifulSoup

import scrapedict as sd

sample = """<html>
<head>
  <title>Page title</title>
</head>
<body>
  <header>
    <h1>Big Header</h1>
  </header>
  <article>
    <p>Paragraph of the article.</p>
  </article>
  <footer><i>Page footer - <a href="http://example.com/">link</a></i></footer>
</body>
</html>"""


@pytest.fixture
def soup():
    return sd.cook(sample)


def test_cook_returns_soup(soup):
    # assumes that the soup fixture uses the cook function

    assert isinstance(soup, BeautifulSoup)


def test_cook_ignores_soup(soup):
    new_soup = sd.cook(soup)

    assert new_soup is soup


def test_html(soup):
    html_header_selector = sd.html("header")

    assert html_header_selector(soup) == soup.header


def test_attr(soup):
    attr_href_selector = sd.attr("a", "href")

    assert attr_href_selector(soup) == soup.a["href"]


def test_text(soup):
    text_h1_selector = sd.text("h1")

    assert text_h1_selector(soup) == soup.h1.string


def test_match(soup):
    parse_article_selector = sd.parse("article", "Paragraph of the {}.")

    assert parse_article_selector(soup)[0] == "article"
