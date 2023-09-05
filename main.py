import requests
from bs4 import BeautifulSoup
import lxml

import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43 '
}

#список под все наши ссылки
fests_urls_list = []

#цикл генерации сылок и отправка запросов от 0 до 192 с шагом 24
# for i in range(0, 192, 24):
for i in range(0, 24, 24):
    url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=17%20Jun%202023&to_date=&genre%5B%5D=pop&maxprice=500&o={i}&bannertitle=July'
    # print(url)

    req = requests.get(url=url, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data['html']

    with open(f'data/index_{i}.html', 'w', encoding='utf-8') as file:
        file.write(html_response)

    #соберем ссылки
    with open(f'data/index_{i}.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    cards = soup.find_all('a', class_='card-details-link')

    for item in cards:
        fest_url = 'https://www.skiddle.com' + item.get('href')
        fests_urls_list.append(fest_url)

# print(fests_urls_list)

#переходим по каждой собранной ссылке и собираем информацию
for url in fests_urls_list:

    req = requests.get(url=url, headers=headers)

    try:
        soup = BeautifulSoup(req.text, 'lxml')
    except Exception as ex:
        print(ex)
        print('Damn...There was some error')
