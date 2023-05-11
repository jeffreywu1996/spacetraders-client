# import sys
# sys.path.append('backend')
import logging

from backend.controllers import marketplace

logger = logging.getLogger(__name__)

def sell_goods():
    logger.info('Selling all goods...')
    cargos = marketplace.list_cargo()
    logger.info(f'Current cargo: {cargos}')

    logger.info('Docking ship...')
    assert marketplace.docking_ship(), 'Ship is not docked'

    logger.info('Selling goods...')
    reciept = marketplace.sell_all_goods(cargos)
    logger.info(reciept)
    logger.info('Selling done.')
