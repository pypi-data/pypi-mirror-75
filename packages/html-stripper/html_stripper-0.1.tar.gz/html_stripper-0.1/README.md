A simple package to extract text from (even broken/invalid) HTML. No dependencies, it just uses Python's internal `HTMLParser` with a few tweaks.

Usage:

```python
from html_stripper import strip_tags

text = strip_tags("<html>…")
```

```python
from html_stripper import strip_tags
import requests
strip_tags(requests.get("https://foo.bar/").text)
```

```python
from html_stripper import strip_tags, strip_newlines

text = strip_newlines(strip_tags("<html>…"))
```
