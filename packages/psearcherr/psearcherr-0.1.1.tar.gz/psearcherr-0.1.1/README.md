# psearcher-r

Rewrite for Python baidu search client: [iridesc/psearcher](https://github.com/iridesc/psearcher)

```python
from psearcherr import Baidu, Bing

for engine in [Baidu(), Bing()]:
  result = engine.search(kw='蝙蝠侠', amount=20)
  print(result)
```

requirements: requests, retry(default 3 times `BaseEngine.n_retry`), beautifulsoup-4(bs4); loger
