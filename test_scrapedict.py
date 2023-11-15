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
    <p>Paragraph of the article.
    
    Force new-line characters into the text.

    âœ” No problem.</p>
    
    <ul class="items">
      <li class="item"><span class="name">Item 1</span><span class="price">9.99</span></li>
      <li class="item"><span class="name">Item 2</span><span class="price">19.99</span></li>
      <li class="item"><span class="name">Item 3</span><span class="price">29.99</span></li>
    </ul>
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
    parse_article_selector = sd.match("article", "Paragraph of the {}.")

    assert parse_article_selector(soup)[0] == "article"


def test_extract_with_rules_dict(soup):
    fields = {
        "title": sd.text("title"),
        "header": sd.text("h1"),
        "article": sd.text("article p"),
        "footer": sd.text("footer"),
    }
    data = sd.extract(fields, soup)

    assert data == {
        "title": "Page title",
        "header": "Big Header",
        "article": "Paragraph of the article. Force new-line characters into the text. ✔ No problem.",
        "footer": "Page footer - link",
    }


def test_extract_all_with_rules_dict(soup):
    fields = {
        "name": sd.text(".name"),
        "price": sd.text(".price"),
    }
    data = sd.extract_all(".item", fields, soup)

    assert data == [
        {"name": "Item 1", "price": "9.99"},
        {"name": "Item 2", "price": "19.99"},
        {"name": "Item 3", "price": "29.99"},
    ]
