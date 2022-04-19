from bs4 import BeautifulSoup
import requests
import json


def subir_json(load_arquivo: str, dados: object) -> str:
    with open(load_arquivo, 'w') as banco:
        json.dump(dados, banco, indent=4, ensure_ascii=False)
        return '*** DADOS ENVIADOS COM SUCESSO ***'


BASE_URL = r'https://g1.globo.com/pa/para'
response = requests.get(BASE_URL)
html_document = response.text

soup = BeautifulSoup(html_document, 'html.parser')

json_return = list()

for news in soup.find_all('a', attrs={'class': 'feed-post-link gui-color-primary gui-color-hover'}):

    link = news['href']
    print(link)
    title = news.text

    response = requests.get(link)
    article = response.text
    soup2 = BeautifulSoup(article, 'html.parser')
    article_datetime = None
    for datetime in soup2.find_all('p', attrs={'class': 'content-publication-data__updated'}):
        article_datetime = datetime.text.strip()

    obj = {"title": title, "link": link, 'date': article_datetime}

    json_return.append(obj)

subir_json('daily_news.json', json_return)
