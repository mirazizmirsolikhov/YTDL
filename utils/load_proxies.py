import json


def load_proxies():
    with open('proxies.json') as f:
        json_data = json.load(f)
    return json_data
