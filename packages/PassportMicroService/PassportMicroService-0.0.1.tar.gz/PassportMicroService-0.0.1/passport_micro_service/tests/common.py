import requests
import json


def post(url, json_data, headers=None, logger=None):
    result = requests.post(
        url=url,
        json=json_data,
        headers=headers
    )
    if result.status_code == 200:
        data = json.loads(result.content.decode('utf-8'))
        if data['code'] == 20000:
            return data['data']
        else:

            return data

    return result
