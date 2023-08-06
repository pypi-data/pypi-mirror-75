from .BaseEngine import BaseEngine, EngineInfo, let

class Baidu(BaseEngine):
  INFO = EngineInfo("Baidu", "http://www.baidu.com/s", "wd", "pn", 0)
  def __init__(self, **kwargs):
    super().__init__(info=Baidu.INFO, **kwargs)

  def parseResult(self, soup):
    text = lambda it: it.text
    def proc(e):
      a = e.h3.a
      d = e.select_one('div .c-span-last')
      res = { 'title': a.getText(), 'link': a['href'] }
      if d != None: res.update({ 'desc': let(text, findCls(d, 'c-abstract')), 'showurl': let(text, d.select_one('.c-showurl')) })
      return res
    return [proc(div) for div in soup.findAll('div', {'class': 'result'})]

def findCls(e, css, tag="div"): return e.find(tag, {"class":css})
