import warnings
from contextlib import suppress

from bs4 import BeautifulSoup
from parse import compile as parse_compile


def cook(html):
    return html if isinstance(html, BeautifulSoup) else BeautifulSoup(html)


def html(selector):
    def html_selector(soup):
        return soup.select_one(selector)

    return html_selector


def attr(selector, attr_name):
    def attr_selector(soup):
        with suppress(TypeError, KeyError):
            return soup.select_one(selector)[attr_name]

    return attr_selector


def text(selector):
    def text_selector(soup):
        with suppress(AttributeError):
            return soup.select_one(selector).get_text()

    return text_selector


def match(selector, pattern):
    compiled_pattern = parse_compile(pattern)

    def parse_selector(soup):
        with suppress(AttributeError, TypeError):
            return compiled_pattern.search(soup.select_one(selector).get_text())

    return parse_selector


def parse(selector, pattern):
    warnings.warn("parse is deprecated, use match instead", DeprecationWarning)

    return match(selector, pattern)


def extract(fields, html_soup=None):
    def extractor(html):
        soup = cook(html)
        with suppress(TypeError):
            return {field: selector(soup) for field, selector in fields.items()}
        return {}

    return extractor(html_soup) if html_soup else extractor


def extract_all(selector, fields, html_soup=None):
    item_extractor = extract(fields)

    def all_extractor(html):
        soup = cook(html)
        with suppress(TypeError):
            return list(map(item_extractor, soup.select(selector)))
        return []

    return all_extractor(html_soup) if html_soup else all_extractor
