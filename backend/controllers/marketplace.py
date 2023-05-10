import json
import requests

from config.meta import SHIP_ID, API_TOKEN

def list_cargo() -> dict:
    """
    List out ship cargo
    """
    res = requests.get(
        f'https://api.spacetraders.io/v2/my/ships/{SHIP_ID}',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        },
    )
    payload = res.json()
    if res.status_code != 200:
        print(f'Unknown error. code = {res.status_code}')
        print(payload)
        raise Exception('Unknown error')

    cargos = payload['data']['cargo']
    return cargos


def docking_ship():
    res = requests.post(
        f'https://api.spacetraders.io/v2/my/ships/{SHIP_ID}/dock',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        },
    )
    payload = res.json()
    if res.status_code != 200:
        print(f'Unknown error. code = {res.status_code}')
        print(payload)
        raise Exception('Unknown error')

    return payload['data']['nav']['status'] == 'DOCKED'


def sell_all_goods(cargos: dict):
    reciept = {
        'credits': 0,
        'goods_sold': []
    }


    for i in cargos['inventory']:
        data = {
            'symbol': i['symbol'],
            'units': i['units']
        }

        res = requests.post(
            f'https://api.spacetraders.io/v2/my/ships/{SHIP_ID}/sell',
            headers={
                'Authorization': f'Bearer {API_TOKEN}',
                'Content-Type': 'application/json'
            },
            data=json.dumps(data)
        )

        print(f'Sold goods, symbol: {data["symbol"]}, units: {data["units"]}, status_code: {res.status_code}')
        print(data)
        reciept['goods_sold'].append({
            'symbol': data['symbol'],
            'units': data['units']
        })

    return reciept
