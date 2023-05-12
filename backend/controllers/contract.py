import time
import json
import requests
import logging

from config.meta import SHIP_ID, API_TOKEN, CONTRACT_ID
import entry


logger = logging.getLogger(__name__)


def deliver(contract_id, ship_id, trade_symbol, units):
    logger.info(f'Delivering contract: {contract_id}')
    payload, status_code = entry.post(
        f'/my/contracts/{contract_id}/deliver',
        data={
            'shipSymbol': ship_id,
            'tradeSymbol': trade_symbol,
            'units': units
        }
    )
    logger.info(f'payload: {payload}, status_code: {status_code}')
    return payload, status_code


def get(contract_id):
    payload, status_code = entry.get(f'/my/contracts/{contract_id}')
    return payload, status_code
