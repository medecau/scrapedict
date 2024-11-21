import warnings
from contextlib import suppress

from bs4 import BeautifulSoup
from ftfy import fix_text as ftfy_fix_text
from normality import collapse_spaces as normality_collapse_spaces
from parse import compile as parse_compile


def cook(html):
    if not isinstance(html, str):
        return html

    try:
        return BeautifulSoup(html, "lxml")
    except Exception:
        return BeautifulSoup(html, "html.parser")


def html(selector):
    def html_selector(soup):
        return soup.select_one(selector)

    return html_selector


def attr(selector, attr_name):
    def attr_selector(soup):
        with suppress(TypeError, KeyError):
            return soup.select_one(selector)[attr_name]

    return attr_selector


def text(selector, fix_text=True, colapse_spaces=True, strip=False):
    def text_selector(soup, strip=strip):
        with suppress(AttributeError):
            txt = soup.select_one(selector).get_text()

            if fix_text:
                txt = ftfy_fix_text(txt)

            if colapse_spaces:
                txt = normality_collapse_spaces(txt)

            if strip:
                warnings.warn(
                    "strip is deprecated, use colapse_spaces instead",
                    DeprecationWarning,
                )
                txt = txt.strip()

            return txt

    return text_selector


def match(selector, pattern):
    compiled_pattern = parse_compile(pattern, case_sensitive=False)

    def parse_selector(soup):
        with suppress(AttributeError, TypeError):
            return compiled_pattern.search(soup.select_one(selector).get_text())

    return parse_selector


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
