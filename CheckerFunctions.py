import requests
from bs4 import BeautifulSoup
import json
import os


if os.path.isfile('data.json'):
    with open('data.json', 'r') as f:
        storage = json.load(f)
else:
    f = open('data.json', 'w')
    f.close()
    storage = {}

# Функция получает ответ сервера и метатеги
def get_url_data(url):
    # Пробуем получить ответ, если 200 - собираем нужные данные, если нет, записываем URL в список "плохих"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',}
    try:
        r = requests.get(url, headers=headers, allow_redirects=False)
    except:
        bad_response = str(url) + ' - Нет ответа'
        return bad_response

    rawhtml = BeautifulSoup(r.text, 'lxml')  # Здесь голая HTML
    # Собираем нужные данные
    response = str(r.status_code)
    print(response)
    if response != '200':
        bad_responce = str(url) + ' - ' + str(response)
        return  bad_responce
    title = rawhtml.title
    if title:
        title = title.text

    h1 = rawhtml.h1
    if h1:
        h1 = h1.text

    canonical = rawhtml.head.find('link', attrs={'rel': 'canonical'})
    if canonical:
        canonical = canonical['href']

    description = rawhtml.head.find('meta', attrs={'name': 'description'})
    if description:
        description = description['content']

    meta_robots = rawhtml.head.select('[name=robots], [name=googlebot], [name=yandex]')
    if meta_robots:
        meta_robots = [i.attrs for i in meta_robots]
    else:
        meta_robots = None

    try: x_robots = r.headers['X-Robots-Tag']
    except Exception: x_robots = None

    # Сохраняем данные в виде словаря
    new_data = {'response': response, 'title': title, 'h1': h1,
                'description': description, 'canonical': canonical, 'meta_robots': meta_robots, 'x_robots_tag': x_robots}
    return new_data

# Функция сравнивает данные каждого URL между записанными в БД,
# если есть разница, записывает новые данные, разницу скидывает в файл
def changes_checker(new_data, url):
    changes = []
    if url not in storage.keys():
        storage[url] = new_data
    else:
        if storage[url] != new_data:
            changes.append("Есть изменения на странице: " + str(url))
            for key, value in storage[url].items():
                if value != new_data[key]:
                    changes.append('Старый {}: {}'.format(key, value))
                    changes.append('Новый {}: {}\n'.format(key, new_data[key]))
            storage[url] = new_data

    with open('data.json', 'w') as f:
        json.dump(storage, f)

    return changes
