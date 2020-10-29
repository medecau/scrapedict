**Scrape HTML to dictionaries**

# Usage overview

1. Define the rules dictionary to extract the right bits
2. Create the extraction function passing in the rules
3. Use the extraction function on the BeautifulSoup object

# Usage examples

0. `cook` the HTML to get a BeautifulSoup objext - here we store it in the `soup` variable
   For this example the string in `sample` will be used as the target HTML - normally you would fetch the HTML with your favorite HTTP library or read from the disk.

```python
from pprint import pprint
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
    <p class="abstract">Paragraph of the article.</p>
    <ol>
      <li>
        <span class='description'>first</span>
        <a href="http://first.example.com">link</a>
      </li>
      <li>
        <span class='description'>second</span>
        <a href="http://second.example.com">link</a>
      </li>
      <li>
        <span class='description'>third</span>
        <a href="http://third.example.com">link</a>
      </li>
    </ol>
  </article>
  <footer><i>Page footer - <a href="http://example.com/">link</a></i></footer>
</body>
</html>"""

soup = sd.cook(sample)
```

## Extract a single item

1. Define a `rules` dictionary

```python
rules = {
    "header": sd.html("header"),
    "article": sd.text(".abstract"),
    "footer_link": sd.attr("footer a", "href"),
}
```

2. Create an extractor function feeding it the rules
_`item_extractor` is a function that knows how to extract your item from any `soup`_

```python
item_extractor = sd.extract(rules)
```

3. Use the extractor function feeding it the soup

```python
item = item_extractor(soup)

pprint(item)
```

_output:_

```python
{'article': '\nParagraph of the article.\n',
 'footer_link': 'http://example.com/',
 'header': <header>
<h1>Big Header</h1>
</header>}
```

## Extract multiple items

1. Define the `rules` to extract *each* item

```python
rules = dict(description=sd.text(".description"), url=sd.attr("a", "href"))
```

2. Create the extractor function passing in a selector where the rules should be applied
_this selector should emmit multiple items_

```python
list_item_extractor = sd.extract_all("article ol li", rules)
```

3. Use the extractor function feeding it the soup

```python
items_list = list_item_extractor(soup)

pprint(items_list)
```

```python
[{'description': 'first', 'url': 'http://first.example.com'},
 {'description': 'second', 'url': 'http://second.example.com'},
 {'description': 'third', 'url': 'http://third.example.com'}]
```

# Testing

For testing use `tox`

_all environments in parallel_
```tox -p```
