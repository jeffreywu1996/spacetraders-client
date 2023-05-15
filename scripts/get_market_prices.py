import sys
sys.path.append('.')
sys.path.append('backend')
import logging

from backend.controllers import marketplace
from backend.controllers import transport
from backend.controllers import contract

logger = logging.getLogger(__name__)

SHIP = 'SUMMERRAINZ-A'
ASTEROID_FIELD = 'X1-DF55-17335A'
QUEST_LOCATION = 'X1-DF55-20250Z'
CONTRACT_ID = 'clhh84b2c17vss60d6okrr8yo'

SYSTEM = 'X1-DF55'
PLANET = 'X1-DF55-20250Z'

ORE_TO_MINE = 'ALUMINUM_ORE'
MINE_UNITS = 60

PLANETS = [
    # 'X1-DF55-20250Z',  # planet
    # 'X1-DF55-89861D',  # moon
    # 'X1-DF55-64862A',  # moon
    # 'X1-DF55-71593D',  # moon

    # 'X1-DF55-52054E',  # planet
    # 'X1-DF55-32376B',  # gas giant
    # 'X1-DF55-69207D',  # orbital station
    # 'X1-DF55-20250Z',  # quest
    'X1-DF55-17335A',  # asteroid field
    # 'X1-DF55-49148D',  # planet

    # 'X1-DF55-24439B',  # jump gate
]


def main():
    # for p in PLANETS:
    #     logger.info('\n----------------------------------------\n')
    #     logger.info(f'Fetching prices for planet: {p}')
    #     payload, status_code = marketplace.get_prices(SYSTEM, p, ORE_TO_MINE)
    #     if status_code == 404:
    #         logger.error(f'No market data for planet: {p}')
    #         continue

    #     for p in payload:
    #         logger.info(f'{p}: {payload[p]}')

    payload, _ = marketplace.get_prices(SYSTEM, ASTEROID_FIELD, ORE_TO_MINE)
    curr_price = payload['purchasePrice']
    logger.info(curr_price)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
    main()
