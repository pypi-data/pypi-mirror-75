import requests
from retry import retry
from bs4 import BeautifulSoup
from loger import makelog

import time, random #timeout
from dataclasses import dataclass

@dataclass
class EngineInfo:
  name: str; url: str
  keyParam: str; pageParam: str
  startIndex: int; indexStep: int = 10

class BaseEngine:
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",   
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"
  }
  n_retries = 3; dt_retries = 2
  def __init__(self, info=None, timeout=5):
    self.session = requests.session(); self.timeout=timeout
    self.info=info; self.keyword = ""
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
    self.results.extend(getPageResults())

  def search(self, kw=None, amount=10):
    if kw != None and kw != self.keyword:
      self.pageNo, self.results = 0, []
      self.keyword = kw #kw=None:keep
    started = time.time()
    while len(self.results) < amount and (time.time() - started) < self.timeout:
      try:
        self._addResult(self.info.url, self.getRequestParams())
        self.pageNo += 1
      except Exception as e:
        makelog(f"Failed to get page! {e}", 1)

    if len(self.results) < amount:
      makelog(f"Search {self.keyword} timed out", 2)
    return self.results

def let(transform, x):
  return transform(x) if x != None else None
