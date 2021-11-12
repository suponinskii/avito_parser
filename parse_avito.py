import requests
from bs4 import BeautifulSoup
import csv

print('Введите название товара')
product = input()

HOST = 'https://www.avito.ru/'
page_part = 'p='
query_part = '&q='
URL = 'https://www.avito.ru/rossiya?'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
FILE = 'avito.csv'

def get_html(url, params=None):
    response = requests.get(URL + page_part + str(1) + query_part + product, headers=HEADERS, params=params)
    return response


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='iva-item-content-UnQQ4')
    total = []
    for item in items:
        total.append({
            'title': item.find('div', class_='iva-item-titleStep-_CxvN').get_text(strip=True),
            'link': HOST + item.find('div', class_='iva-item-titleStep-_CxvN').find('a').get('href'),
            'price': item.find('span', class_='price-text-E1Y7h text-text-LurtD text-size-s-BxGpL').get_text().replace('\u20bd','')
        })
    return(total)


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
        total_pages = pages.split('=')[1].split('&')[0]
        return int(total_pages)
    except:
        return 1


def save_doc(total, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Название', 'Цена', 'Ссылка'])
        for item in total:
            writer.writerow([item['title'], item['link'], item['price']])


def parse():
    html = get_html(URL + page_part + str(1) + query_part + product)
    if html.status_code == 200:
        pages_count = get_pages_count(html.text)
        total = []
        for page in range(1, pages_count+1):
            print(f'Парсинг{page} из {pages_count}...')
            url_gen = URL + page_part + str(page) + query_part + product
            html = get_html(url_gen, params=None)
            total.extend(get_content(html.text))
        save_doc(total, FILE)
    else:
        print('Error')


parse()



