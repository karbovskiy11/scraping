import random
from os import mkdir

from bs4 import BeautifulSoup
import requests
import certifi
import json
import time
import os


def get_json(url):
    response = requests.get(url=url, verify=False)
    # response.raise_for_status()
    return response.json()


def save_data(id_data, data):
    os.makedirs('data', exist_ok=True)
    with open(f'data/{id}_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def load_date():
    with open('id_data.json', 'r', encoding='utf-8') as json_file:
        id_data = json.load(json_file)

    points = id_data['data']['points']
    return points


def get_id(data):
    id_comissariates = []
    for point in data:
        id_point = point['id']
        id_comissariates.append(get_data(id_point))

    return id_comissariates


def get_data(data):
    api_url = f'https://mil.ru/api/ssp-maps/point/{data}'
    return api_url




def main():
    api_url = 'https://mil.ru/api/ssp-maps/992a7991-05f0-433c-988f-ff28c9a1aaa8'
    # headers = {
    #     'accept': 'application/json',
    #     'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0'
    # }
    idd = 0
    id_comissariates = get_json(api_url)
    save_data(idd, id_comissariates)
    id_date = load_date()
    id_comissariates = get_id(id_date)

    spisok_comissariates = []
    for item in id_comissariates:
        point = get_json(item)
        spisok = {
                'type': point['data']['type'],
                'title': point['data']['title'],
                'info': point['data']['text_before'],
        }

        spisok_comissariates.append(spisok)
        # save_data()
        print(spisok)
        time.sleep(random.randrange(2, 4))



if __name__ == '__main__':
    main()
