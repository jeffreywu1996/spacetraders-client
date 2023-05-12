import sys
sys.path.append('backend')
import time
import logging

from backend.controllers import marketplace
from backend.controllers import transport
from backend.controllers import contract

logger = logging.getLogger(__name__)

SHIP = 'SUMMERRAINZ-A'
SYSTEM = 'X1-DF55'
ASTEROID_FIELD = 'X1-DF55-17335A'
QUEST_LOCATION = 'X1-DF55-20250Z'
CONTRACT_ID = 'clhh84b2c17vss60d6okrr8yo'

ORE_TO_MINE = 'ALUMINUM_ORE'
MINE_UNITS = 60

BUY_THRESHOLD = 30


deliver_count = 0

def deliever_goods():
    global deliver_count
    while True:
        # check current market prices
        logger.info(f'Checking current market prices for {ORE_TO_MINE}')
        payload, _ = marketplace.get_prices(SYSTEM, ASTEROID_FIELD, ORE_TO_MINE)
        logger.info(payload)
        curr_price = payload['purchasePrice']

        if curr_price >= BUY_THRESHOLD:
            logger.info(f'Too expensive, waiting for price to drop... threshold: {BUY_THRESHOLD}, current price: {curr_price}, waiting 60 seconds...')
            time.sleep(60)
            continue


        logger.info(f'Start delievering goods... {SHIP}, deliver count: {deliver_count}')

        con, _ = contract.get(CONTRACT_ID)
        units_fulfilled = con['data']['terms']['deliver'][0]['unitsFulfilled']
        units_required = con['data']['terms']['deliver'][0]['unitsRequired']
        logger.info(f'Units required: {units_required}, units fulfilled: {units_fulfilled}')
        if units_required <= units_fulfilled - 5:
            logger.info('DONE!')
            return

        transport.fly_to(SHIP, ASTEROID_FIELD)
        transport.dock(SHIP)
        curr_fuel = transport.get_fuel(SHIP)
        logger.info(f"Current fuel: {curr_fuel}")

        if curr_fuel < 100:
            recipt, status_code = transport.refuel(SHIP)
            logger.info(f"refuel cost: {recipt['data']['fuel']}")

        marketplace.purchase(SHIP, ORE_TO_MINE, MINE_UNITS)
        transport.fly_to(SHIP, QUEST_LOCATION)
        transport.dock(SHIP)
        curr_fuel = transport.get_fuel(SHIP)
        logger.info(f"Current fuel: {curr_fuel}")

        payload, status_code = contract.deliver(CONTRACT_ID, SHIP, ORE_TO_MINE, MINE_UNITS)

        if status_code == 400:
            logger.error(f"Failed to deliver contract: {CONTRACT_ID}")
            logger.error(f'payload: {payload}, status_code: {status_code}')
            return

        _contract = payload['data']['contract']
        deliver = _contract['terms']['deliver'][0]
        units_required = deliver['unitsRequired']
        units_fulfilled = deliver['unitsFulfilled']
        deadline = _contract['terms']['deadline']
        logger.info(f"Accepted: {_contract['accepted']}, unitsRequired: {units_required}, unitsFulfilled: {units_fulfilled}, deadline: {deadline}")

        deliver_count += 1



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
    deliever_goods()
