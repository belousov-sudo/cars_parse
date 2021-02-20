# программа парсит данные с сайта AUTO RIA
# программа не моя, я написал её, посмотрев видео на ютубе
# теперь использую как шаблон

import requests
from bs4 import BeautifulSoup
import csv


URL = "https://auto.ria.com/newauto/marka-audi/"
HEADERS = {"user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
           "accept": "*/*"}
HOST = "https://auto.ria.com"
FILE = 'cars.csv'


# получение html разметки страницы по адресу url
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# функция считает, сколько страниц на сайте
def get_pages_count(html):
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find_all('span', class_='page-item mhide')
    if pagination:
        return int(pagination[-1].get_text())
    return 1


# функция получает HTML код страницы и получает список всех нужных данных
def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_='proposition')

    cars = []
    for item in items:
        uah_price = item.find('span', class_='grey size13')
        if uah_price:
            uah_price = uah_price.get_text(strip=True)
        else:
            uah_price = 'Цена не указана.'
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'usd_price': item.find('span', class_='green').get_text(strip=True),
            'uah_price': uah_price,
            'city': item.find('div', class_='proposition_region size13').find_next('strong').get_text(strip=True)
        })
    return cars


# функция получает все данные парсинга и помещает их по пути path
def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Цена в $', 'Цена в грн.', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['usd_price'],
                             item['uah_price'], item['city']])


# функция автоматически открывает созданный файл (работает на всех операционных системах)
def open_file(path):
    pass


# основная функция программы
def parse():
    URL = input('Введите URL: ').strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f"Парсинг страницы {page} из {pages_count}...")
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        print(f"Получено {len(cars)} автомобилей.")
        save_file(cars, FILE)
        open_file(FILE)
    else:
        print("Error")


parse()
