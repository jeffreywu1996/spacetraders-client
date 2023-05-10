import json
import requests

from config.meta import SHIP_ID, API_TOKEN

def start():
    res = requests.post(
        f'https://api.spacetraders.io/v2/my/ships/{SHIP_ID}/extract',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        },
    )
    payload = res.json()
    if res.status_code == 201:
        print(f"Mining successful, wait {payload['data']['cooldown']['remainingSeconds']} seconds")
    elif res.status_code == 409:
        print(f"Mining in progrress. message: {payload['error']['message']}, wait: {payload['error']['data']['cooldown']['remainingSeconds']} seconds")
    elif res.status_code == 400:
        print(f"Mining in progrress. message: {payload['error']['message']}, wait: {payload['error']['data']['cooldown']['remainingSeconds']} seconds")
    else:
        print(f'Unknown error. code = {res.status_code}')
        print(payload)
