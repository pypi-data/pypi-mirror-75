import requests
from retry import retry
from bs4 import BeautifulSoup
from loger import setting as loger_setting, makelog

import time, random #timeout

class EngineInfo:
  def __init__(self, name, url, p_kw, p_pn, idx_z, idx_step=10):
    self.name, self.url, = name, url
    self.keyParam, self.pageParam = p_kw, p_pn
    self.startIndex, self.indexStep = idx_z, idx_step

class BaseEngine:
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",   
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"
  }
  n_retries = 3; dt_retries = 2
  def __init__(self, kw, info=None, timeout=10):
    self.session = requests.session(); self.timeout=timeout
    self.info=info; self.keyword=kw
    self.pageNo = 0; self.results = []

  def parseResult(self, soup) -> list: raise NotImplementedError()

  def getRequestParams(self):
    c = self.info
    return {
      c.keyParam: self.keyword,
      c.pageParam: c.startIndex + c.indexStep*self.pageNo,
    }

  def _addResult(self, url, params):
    @retry(tries=BaseEngine.n_retries, delay=random.random()*BaseEngine.dt_retries)
    def getPageResults():
      resp = self.session.get(url, params=params, headers=BaseEngine.headers)
      try: resp.raise_for_status()
      except: makelog(f"Connection error", 2)
      soup = BeautifulSoup(resp.text, "html.parser")
      res = self.parseResult(soup)
      if (len(res) == 0):
        makelog(f"Parse fail: {url} {params}", 2)
        with open("error.html", "w+") as f: f.write(resp.text)
        raise Exception() #fail once
      return res

    makelog(f"{self.info.name} {self.keyword} #{self.pageNo} n={len(self.results)}")
    try: self.results.extend(getPageResults())
    except Exception as e:
      makelog(f"Failed to get page! {e}", 1)

  def search(self, amount=5):
    started = time.time()
    while len(self.results) < amount and (time.time() - started) < self.timeout:
      self._addResult(self.info.url, self.getRequestParams())
      self.pageNo += 1

    if len(self.results) < amount:
      makelog(f"Search {self.keyword} timed out", 2)
    return self.results
