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
import scrapedict as sd
from urllib.request import urlopen

# Fetch the content from the Urban Dictionary page for "larping"
url = "https://www.urbandictionary.com/define.php?term=larping"
content = urlopen(url).read().decode()

# Define the fields to be extracted
fields = {
    "word": sd.text(".word"),
    "meaning": sd.text(".meaning"),
    "example": sd.text(".example"),
}

# Extract the data using scrapedict
item = sd.extract(fields, content)

# The result is a dictionary with the word, its meaning, and an example usage.
# Here, we perform a couple of assertions to demonstrate the expected structure and content.
assert isinstance(item, dict)
assert item["word"].lower() == "larping"
```


# The orange site example

```python
import scrapedict as sd
from urllib.request import urlopen

# Fetch the content from the Hacker News homepage
url = "https://news.ycombinator.com/"
content = urlopen(url).read().decode()

# Define the fields to extract: title and URL for each news item
fields = {
    "title": sd.text(".titleline a"),
    "url": sd.attr(".titleline a", "href"),
}

# Use scrapedict to extract all news items as a list of dictionaries
items = sd.extract_all(".athing", fields, content)

# The result is a list of dictionaries, each containing the title and URL of a news item.
# Here, we assert that 30 items are extracted, which is the expected number of news items on the Hacker News homepage.
assert len(items) == 30
```


# Development

Dependencies are managed with [uv](https://github.com/astral-sh/uv).
Testing is done with [Tox](https://tox.readthedocs.io/en/latest/).
