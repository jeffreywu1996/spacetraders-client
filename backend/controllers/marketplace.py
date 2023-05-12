import requests
import logging

from config.meta import SHIP_ID
import entry

logger = logging.getLogger(__name__)

def get_prices(system: str, waypoint: str, item: str):
    try:
        payload, status_code = entry.get(f'/systems/{system}/waypoints/{waypoint}/market')
        # logger.info(f'payload: {payload}, status_code: {status_code}')
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.error(e.response.json())
            return e.response.json(), 404
        raise e

    if 'tradeGoods' not in payload['data']:
        return payload, 404

    trade_goods = payload['data']['tradeGoods']

    for good in trade_goods:
        if good['symbol'] == item:
            return good, status_code

    return payload, 404


def list_cargo() -> dict:
    """
    List out ship cargo
    """
    payload, status_code = entry.get(f'/my/ships/{SHIP_ID}')
    return payload['data']['cargo']


def docking_ship():
    payload, status_code = entry.post(f'/my/ships/{SHIP_ID}/dock')
    return payload['data']['nav']['status'] == 'DOCKED'


def purchase(ship_id, symbol, units):
    logger.info(f'Purchasing goods, ship_id: {ship_id}, symbol: {symbol}, units: {units}...')
    payload, status_code = entry.post(
        f'/my/ships/{ship_id}/purchase',
        data={
            'symbol': symbol,
            'units': units
        }
    )
    logger.info(f'payload: {payload}, status_code: {status_code}')

    return payload, status_code



def sell_all_goods(cargos: dict):
    reciept = {
        'credits': 0,
        'goods_sold': []
    }


    for i in cargos['inventory']:
        data={
            'symbol': i['symbol'],
            'units': i['units']
        }

        payload, status_code = entry.post(
            f'/my/ships/{SHIP_ID}/sell',
            data=data
        )

        if status_code in [200, 201]:
            trans = payload['data']['transaction']
            logger.info(f'Sold goods, symbol: {data["symbol"]}, units: {data["units"]}, price per unit: {trans["pricePerUnit"]}, profit: {trans["totalPrice"]}, status_code: {status_code}')
            reciept['goods_sold'].append({
                'symbol': data['symbol'],
                'units': data['units']
            })

        else:
            logger.info(f'Cannot sel goods, symbol: {data["symbol"]}, units: {data["units"]}, status_code: {status_code}')

    return reciept
