from .BaseEngine import BaseEngine, EngineInfo
class Bing(BaseEngine):
  INFO = EngineInfo("Bing", "http://www.bing.com/search", "q", "first", 1)
  def __init__(self, **kwargs):
    super().__init__(info=Bing.INFO, **kwargs)

  def parseResult(self, soup):
    def proc(e):
      h = e.h2
      return { 'title': h.getText(strip=True), 'link': h.a['href'],
        'desc': e.find('p').text }
    return [proc(li) for li in soup.findAll('li', {'class': 'b_algo'})]
