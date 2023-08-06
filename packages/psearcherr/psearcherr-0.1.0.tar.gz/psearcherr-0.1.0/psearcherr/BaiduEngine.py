from .BaseEngine import BaseEngine, EngineInfo
class Baidu(BaseEngine):
  INFO = EngineInfo("Baidu", "http://www.baidu.com/s", "word", "pn", 0)
  def __init__(self, kw, **kwargs):
    super().__init__(kw, info=Baidu.INFO, **kwargs)

  def parseResult(self, soup):
    def post(e):
      a = e.h3.a
      return { 'title': a.getText(), 'link': a['href'] }
    return [post(div) for div in soup.findAll('div', {'class': 'result'})]
