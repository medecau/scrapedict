from contextlib import suppress

from bs4 import BeautifulSoup
from parse import compile as compile_parse_pattern


def cook(html):
    return BeautifulSoup(html)


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


def parse(selector, pattern):
    compiled_pattern = compile_parse_pattern(pattern)

    def parse_selector(soup):
        with suppress(AttributeError, TypeError):
            return compiled_pattern.search(soup.select_one(selector).get_text())

    return parse_selector


def extract(fields):
    def extractor(soup):
        with suppress(TypeError):
            return {field: selector(soup) for field, selector in fields.items()}
        return {}

    return extractor


def extract_all(selector, fields):
    def extract_all_selector(soup):
        with suppress(TypeError):
            return list(map(extract(fields), soup.select(selector)))
        return []

    return extract_all_selector
