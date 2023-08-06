from .BaseEngine import BaseEngine, EngineInfo
class Bing(BaseEngine):
  INFO = EngineInfo("Bing", "http://www.bing.com/search", "q", "first", 1)
  def __init__(self, kw, **kwargs):
    super().__init__(kw, info=Bing.INFO, **kwargs)

  def parseResult(self, soup):
    def post(e):
      h = e.h2
      return { 'title': h.text.strip(), 'link': h.a['href'],
        'desc': e.find('p').text }
    return [post(li) for li in soup.findAll('li', {'class': 'b_algo'})]