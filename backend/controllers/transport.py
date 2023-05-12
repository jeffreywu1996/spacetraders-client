import time
import logging

from utils import secs_until_iso_date
import entry


logger = logging.getLogger(__name__)


def fly_to(ship_id: str, waypoint: str, wait=True) -> dict:
    logger.info(f'Flying ship: {ship_id} to waypoint: {waypoint} ...')
    payload, status_code = entry.post(
        f'/my/ships/{ship_id}/navigate',
        data={'waypointSymbol': waypoint}
    )

    logger.info(f'payload: {payload}, status_code: {status_code}')
    if status_code == 400:
        logger.warning(payload['error']['message'])
        return payload, status_code

    arrival = payload['data']['nav']['route']['arrival']
    secs_til_arrival = secs_until_iso_date(arrival)
    logger.info(f'Will arrive in: {secs_til_arrival} seconds')

    if wait:
        logger.info('Waiting for arrival ...')
        time.sleep(secs_til_arrival)
        logger.info('Arrived at destination')

    return payload, status_code


def dock(ship_id: str):
    payload, status_code = entry.post(f'/my/ships/{ship_id}/dock')
    docked = payload['data']['nav']['status'] == 'DOCKED'
    if docked:
        logger.info(f'{ship_id} docked successfully')
    else:
        logger.error(f'{ship_id} failed to dock, payload: {payload}, status_code: {status_code}')


def get_fuel(ship_id: str):
    payload, status_code = entry.get(f'/my/ships/{ship_id}')
    # logger.info(f'payload: {payload}, status_code: {status_code}')
    return payload['data']['fuel'], status_code


def refuel(ship_id: str):
    logger.info(f'Refueling ship: {ship_id} ...')
    payload, status_code = entry.post(f'/my/ships/{ship_id}/refuel')
    # logger.info(f'payload: {payload}, status_code: {status_code}')
    return payload, status_code


def get_waypoint_symbol(ship_id: str):
    payload, status_code = entry.get(f'/my/ships/{ship_id}')
    # logger.info(f'payload: {payload}, status_code: {status_code}')
    return payload['data']['nav']['waypointSymbol'], status_code
