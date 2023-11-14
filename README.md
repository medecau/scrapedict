*Write scraping rules, get dictionaries.*

`scrapedict` is a Python module designed to simplify the process of writing web scraping code. The goal is to make scrapers easy to adapt and maintain, with straightforward and readable code.


# Features

- The rules dictionary is straightforward and easy to read
- Once you define the rules for one item you can extract multiple items
- You get ✨dictionaries✨ of the data you want


# Installation

```$ pip install scrapedict```


# Usage

```python
import requests
import scrapedict as sd

response = requests.get("https://www.urbandictionary.com/define.php?term=larping")

fields = {
    "word": sd.text(".word"),
    "meaning": sd.text(".meaning"),
    "example": sd.text(".example"),
}

item = sd.extract(fields, response.text)
```


# The orange site example

```python
import requests
import scrapedict as sd

response = requests.get("https://news.ycombinator.com/")

fields = {
    "title": sd.text(".titleline a"),
    "url": sd.attr(".titleline a", "href"),
}

items = sd.extract_all(".athing", fields, response.text)
```


# Development

Dependencies are managed with [Poetry](https://python-poetry.org/).

Testing is done with [Tox](https://tox.readthedocs.io/en/latest/).
