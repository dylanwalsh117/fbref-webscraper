import requests
from bs4 import BeautifulSoup
import warnings
import json


def convert_metrics(data):
    data = data.split("'")

    fixed_arr = []

    for number in data:

        try:
            if number[-1] == '%':
                fixed_arr.append(float(number.split('%')[0]))
        except Exception as e:
            # print('Not a percentage')
            pass

        try:
            fixed_arr.append(float(number))
        except Exception as e:
            pass

    return fixed_arr


def convert_names(data):
    return [element for elem_list in data for element in elem_list]


def convert_to_data_obj(labels_arr, data_arr):
    data_obj = {}

    for idx, element in enumerate(labels_arr):
        data_obj[element] = data_arr[idx]

    return data_obj


def get_player_data(x):
    warnings.filterwarnings("ignore")
    url = x
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    name = [element.text for element in soup.find_all("span")]
    name = name[7]
    metric_names = []
    metric_values = []

    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        first_column = row.findAll('th')[0].contents
        metric_names.append(first_column)
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        first_column = row.findAll('td')[0].contents
        metric_values.append(first_column)

    metric_values = repr(metric_values)
    metric_values = convert_metrics(metric_values)
    metric_names = convert_names(metric_names)

    player_data_obj = convert_to_data_obj(metric_names, metric_values)

    player_data_obj['name'] = name

    with open('output.json', 'a') as outfile:
        outfile.write(json.dumps(player_data_obj, indent=4))

    return player_data_obj


get_player_data("https://fbref.com/en/players/867239d3/Paul-Pogba")
