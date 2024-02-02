from typing import List
from haystack import component, Document
from newspaper import Article
import requests

@component
class HackernewsFetcher():

  @component.output_types(articles=List[Document])
  def run(self, top_k: int):
    newest_list = requests.get(url='https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    articles = []
    for id in newest_list.json()[0:top_k]:
      article = requests.get(url=f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty")
      if 'url' in article.json():
        articles.append(article.json()['url'])

    docs = []
    for url in articles:
      try:
        article = Article(url)
        article.download()
        article.parse()
        docs.append(Document(content=article.text, meta={'title': article.title, 'url': url}))
      except:
        print(f"Couldn't download {url}, skipped")
    return {'articles': docs}
