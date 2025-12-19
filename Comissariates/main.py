import csv
import json
import os
import random
import re
import time
import warnings

import requests
from urllib3.exceptions import InsecureRequestWarning


def get_json(url):
    try:
        warnings.simplefilter('ignore', InsecureRequestWarning)
        response = requests.get(url=url, verify=False, timeout=5)
        time.sleep(random.randrange(2, 5))
        if response.status_code == 200:
            print(f"✓ API доступен: код {response.status_code}")
        elif response.status_code in [401, 403]:
            print(f"⚠ API требует аутентификации: {response.status_code}")
        elif response.status_code == 404:
            print(f"✗ API не найден: {response.status_code}")
        elif response.status_code >= 500:
            print(f"✗ Проблемы с сервером: {response.status_code}")
        else:
            print(f"? Неожиданный статус: {response.status_code}")
        return response.json()
    except requests.exceptions.ConnectionError:
        print("✗ Не удалось подключиться к API")
    except requests.exceptions.Timeout:
        print("✗ Таймаут при подключении к API")
    except requests.exceptions.RequestException as e:
        print(f"✗ Ошибка: {e}")



def save_json(name, data):
    os.makedirs('data', exist_ok=True)
    with open(f'data/{name}_comissariates.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def load_date():
    with open(f'data/id_comissariates.json', 'r', encoding='utf-8') as json_file:
        id_data = json.load(json_file)
    return id_data


def get_id(data):
    id_comissariates = []
    for point in data:
        id_point = point['id']
        id_comissariates.append(get_data(id_point))

    return id_comissariates


def get_data(data):
    api_url = f'https://mil.ru/api/ssp-maps/point/{data}'
    return api_url


def create_csv():
    with open('data/comissariates.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(
            [
                '№',
                'Тип',
                'Наименование',
                'Адрес',
                'Телефон',
                'Время работы'
            ]
        )


def save_in_csv(data):
    with open('data/comissariates.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data.values())


def clean_symbol(data):
    clean_info = re.sub(r'<[^>]+>', '', data)
    return clean_info


def main():
    api_url = 'https://mil.ru/api/ssp-maps/992a7991-05f0-433c-988f-ff28c9a1aaa8'
    id_comissariates = get_json(api_url)
    if id_comissariates:
        print(f'id военкоматов получены.')
        name = 'id'
        save_json(name, id_comissariates['data']['points'])
        id_date = load_date()
        id_comissariates = get_id(id_date)
        create_csv()
        spisok_comissariates = []

        count = 1
        for item in id_comissariates:
        # if count < 4:
            point = get_json(item)
            if point is not True:
                print(f'Данные от военкомата № {count} не получены.')
                break
            data_type = point['data']['type']
            data_title = point['data']['title']
            data_info = [clean_symbol(i) for i in point['data']['text_before'].split('<br>') if i != '']
            try:
                data_address = data_info[0]
                # print(f'{data_address}')
            except IndexError:
                data_address = 'Информация отсутствует'
            try:
                data_telefon = data_info[1]
                # print(f'{data_telefon}')
            except IndexError:
                data_telefon = 'Информация отсутствует'
            try:
                data_time = data_info[2]
                # print(f'{data_time}')
            except IndexError:
                data_time = 'Информация отсутствует'
            spisok = {
                '№': count,
                'Тип': data_type,
                'Наименование': data_title,
                'Адрес': data_address.replace('Адрес: ', ''),
                'Телефон': data_telefon.replace('Телефон: ', ''),
                'Время работы': data_time.replace('Время работы: ', ''),
            }
            spisok_comissariates.append(spisok)
            print(f'Информация о военкомате № {count} собрана.')
            save_in_csv(spisok)
            name = 'spisok'
            count += 1

        # else:
        #     break

        save_json(name, spisok_comissariates)


if __name__ == '__main__':
    main()
