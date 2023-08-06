import requests
import json


def post(url, json_data, headers=None, logger=None):
    # print('post: ', url)
    result = requests.post(
        url=url,
        json=json_data,
        headers=headers
    )
    if result.status_code == 200:
        data = json.loads(result.content.decode('utf-8'))
        # print('data: ', data)
        return data
    return result


def app_post(client, url, json_data):
    return post(
        url='%s%s' % (client.passport_service_url, url),
        json_data=json_data,
        headers={
            'X-AccessToken': client.access_token
        }
    )
