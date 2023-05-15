import sys
sys.path.append('backend')

import time
import logging

from sell_goods import sell_goods
from backend.config.meta import SHIP_ID
from backend import entry
from backend.controllers import transport
from backend.controllers import systems

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)

# MINE_LOCATION = 'X1-DF55-17335A'


def main():
    mine_count = 0

    logger.info(f'Start mining operations on {SHIP_ID} ...')
    # logger.info('Find mine location...')
    # payload, _ = systems.list_systems(type='ASTEROID_FIELD')
    # asteroid_field = payload['waypoints'][0]['symbol']
    # logger.info(f'Found asteroid field: {asteroid_field}')
    # MINE_LOCATION = asteroid_field
    MINE_LOCATION = 'X1-ZA40-99095A'

    if transport.get_waypoint_symbol(SHIP_ID) != MINE_LOCATION:
        transport.fly_to(SHIP_ID, MINE_LOCATION)

    # print current inventory
    payload, status_code = entry.get(f'/my/ships/{SHIP_ID}')
    cargo = payload['data']['cargo']
    logger.info(f"current cargo capcity: {cargo['units']} / {cargo['capacity']}")
    inventory = [{'symbol': c['symbol'], 'units': c['units']} for c in cargo['inventory']]
    logger.info(f"inventory: {inventory}")

    while True:
        logger.info(f'Start mining... {SHIP_ID}, mine count: {mine_count}')
        payload, status_code = entry.post(f'/my/ships/{SHIP_ID}/extract')

        if status_code == 201:
            # Successful mine. Wait for cooldown, check cargo and continue
            wait = payload['data']['cooldown']['remainingSeconds']
            logger.info(f"Started mining successful, waiting {payload['data']['cooldown']['remainingSeconds']} seconds until complete...")
            time.sleep(wait)

            payload, status_code = entry.get(f'/my/ships/{SHIP_ID}')
            cargo = payload['data']['cargo']
            inventory = [{'symbol': c['symbol'], 'units': c['units']} for c in cargo['inventory']]
            logger.info(f"current cargo capcity: {cargo['units']} / {cargo['capacity']}")
            logger.info(f"inventory: {inventory}")
            mine_count += 1

        elif status_code == 409:
            #  Mining already in progress. Wait for cooldown and retry mining
            logger.warning(payload)
            try:
                wait = payload['error']['data']['cooldown']['remainingSeconds']
            except KeyError:
                wait = -1
            logger.warning(f"Mining is already in progress. message: {payload['error']['message']}, will wait: {wait} seconds until next try")
            time.sleep(wait)

        elif status_code == 400:
            # Max cargo reached. Sell goods and continue
            logger.warning(f"Max cargo reached, cannot mine anymore")
            logger.warning(payload)

            time.sleep(1)
            sell_goods()
            time.sleep(1)
            logger.info("Goods sold, continue mining...")

        else:
            logger.error(f'Unknown error. code = {status_code}')
            logger.error(payload)
            time.sleep(60)


if __name__ == '__main__':
    main()
