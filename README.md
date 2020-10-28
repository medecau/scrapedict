Scrape HTML to dictionaries

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
    <p>Paragraph of the article.</p>
  </article>
  <footer><i>Page footer - <a href="http://example.com/">link</a></i></footer>
</body>
</html>"""


# create an extractor by defining dictionary where the values are
# css selectors of the bits you want
item_extractor = sd.extract({
    'header': sd.html('header'),
    'article': sd.text('article'),
    'footer_link': sd.attr('footer a', 'href')
    })

# fetch the HTML with your favorite HTTP lib or read from the disk
# then get a BeautifulSoup object
soup = sd.cook(sample)

# feed the soup to your extractor
item = item_extractor(soup)

# get a dictinary
pprint(item)
```

```python
{'article': '\nParagraph of the article.\n',
 'footer_link': 'http://example.com/',
 'header': <header>
<h1>Big Header</h1>
</header>}
```

