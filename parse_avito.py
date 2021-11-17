import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://kolesa.kz/cars/avtomobili-s-probegom/?page='
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
FILE = 'kolesa_kz.csv'

def get_html(url, params=None):
    response = requests.get(URL + str(1), headers=HEADERS, params=params)
    return response


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='a-info-side col-right-list')
    total = []
    for item in items:
        total.append({
            'title': item.find('span', class_='a-el-info-title').get_text(strip=True),
            'description': item.find('div', class_='a-search-description').get_text(strip=True)[:4]
        })
    return(total)


def save_doc(total, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Название', 'Год'])
        for item in total:
            writer.writerow([item['title'], item['description']])


def parse():
    html = get_html(URL + str(1))
    if html.status_code == 200:
        total = []
        for page in range(1, 1000):
            print(f'Парсинг{page} из 1000')
            url_gen = URL + str(page)
            html = get_html(url_gen, params=None)
            total.extend(get_content(html.text))
        save_doc(total, FILE)
    else:
        print('Error')


parse()
