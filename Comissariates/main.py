from bs4 import BeautifulSoup
import requests
import certifi
import json


def get_json(url, headers):
    response = requests.get(url=url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()


def save_data(data):
    with open('id_data.json', 'w', encoding='utf-8') as json_file:
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
        id_comissariates.append(id_point)

    return id_comissariates


def main():
    url = 'https://mil.ru/api/ssp-maps/992a7991-05f0-433c-988f-ff28c9a1aaa8'
    headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0'
    }

    # id_comissariates = get_json(url, headers)
    # save_data(id_comissariates)
    id_date = load_date()
    id_comissariates = get_id(id_date)
    print(id_comissariates)


if __name__ == '__main__':
    main()
