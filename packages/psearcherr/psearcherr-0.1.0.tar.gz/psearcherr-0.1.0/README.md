# psearcher-r

Rewrite for Python baidu search client: [iridesc/psearcher](https://github.com/iridesc/psearcher)

```python
from psearcherr import Baidu
from psearcherr import Bing

for engine in [Baidu(kw='蝙蝠侠'), Bing(kw='蝙蝠侠 黑暗骑士')]:
  result = engine.search(amount=20)
  print(result)
```
