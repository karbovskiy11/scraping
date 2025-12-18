import random
import re
from os import mkdir

from bs4 import BeautifulSoup
import requests
import certifi
import json
import time
import os
import csv


def get_json(url):
    response = requests.get(url=url, verify=False)
    # response.raise_for_status()

    # save_data(idd, response.json())
    return response.json()


def save_json(name, data):
    os.makedirs('data', exist_ok=True)
    with open(f'data/{name}_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def load_date(name):
    with open(f'data/{name}_data.json', 'r', encoding='utf-8') as json_file:
        id_data = json.load(json_file)

    points = id_data
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

def save_csv(data):
    with open('data/comissariates.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(data)


def main():
    api_url = 'https://mil.ru/api/ssp-maps/992a7991-05f0-433c-988f-ff28c9a1aaa8'
    # headers = {
    #     'accept': 'application/json',
    #     'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0'
    # }
    # idd = 0
    # id_comissariates = get_json(api_url)
    name = 'id'
    # save_json(name, id_comissariates['data']['points'])
    id_date = load_date(name)
    id_comissariates = get_id(id_date)

    spisok_comissariates = []
    # idd = 1
    count = 0
    for item in id_comissariates:
        if count < 4:
            point = get_json(item)
            # spisok = {
            #         'type': point['data']['type'],
            #         'title': point['data']['title'],
            #         'info': point['data']['text_before'],
            # }

            point_info = point['data']['text_before']
            clean_info = re.sub(r'<[^>]+>', '', point_info)
            spisok = [
                    point['data']['type'],
                    point['data']['title'],
                    clean_info

            ]

            spisok_comissariates.append(spisok)

            print(spisok)
            count += 1
            time.sleep(random.randrange(2, 4))
        else:
            break


    name = 'spisok'
    # save_json(name, spisok_comissariates)
    save_csv(spisok_comissariates)


if __name__ == '__main__':
    main()
