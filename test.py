__author__ = 'Vlad'
import requests
import json
from fuzzywuzzy import process
import time
import os
# region constants
SUBJECTS = ['Українська мова та література',
            'Історія України',
            'Математика',
            'Фізика',
            'Хімія',
            'Біологія',
            'Географія',
            'Англійська мова',
            'Французька мова',
            'Німецька мова',
            'Іспанська мова',
            'Російська мова',
            'Всесвітня історія',
            'Світова література']

PATH = [r'E:\ZNO\ZNO2010',
        r'E:\ZNO\ZNO2011',
        r'E:\ZNO\ZNO2012',
        r'E:\ZNO\ZNO2013',
        r'E:\ZNO\ZNO2014']

# endregion

def test_subjects(path):
    for sub in SUBJECTS:
        n = 0
        for filename in os.listdir(path):
            if '.xls' in filename and ',' in filename and sub in filename:
                n += 1
        print(sub, n)

def fuzzy_test():
    schools = []
    data_file = open('schools.json', 'r', encoding='UTF-8')
    data = json.load(data_file)
    for elem in data['objects']:
        schools.append(elem['name'])
    # print(schools[1])


    print(process.extract("Косівський", schools, limit=5))

def request_test():

    start_time = time.time()
    # filters = [(dict(name='school', op='has', val={'name':'area', 'op':'ilike', 'val':'%%'}))]

    filters = {}
    url = 'http://127.0.0.1:5000/api/v2/results'
    headers = {'Content-Type': 'application/json'}
    # functions = [{"name": "count", "field": "id"}]

    params = dict(q=json.dumps(dict(filters=filters)))#, page=1)
    # params = dict(q=json.dumps(dict(functions=functions)))

    params = {}
    response = requests.get(url, params=params, headers=headers)
    # print(params)
    # print(response.text)
    if response.status_code == 200:
        print(response.json()['objects'])
        n = response.json()["total_pages"]
        print(response.status_code)
        print(n)
        print("--- {0} seconds ---".format((time.time() - start_time)*n))
    else:
        print('error')
        print("--- {0} seconds ---".format((time.time() - start_time)))

if __name__ == "__main__":
    request_test()
