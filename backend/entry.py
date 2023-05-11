import json
import logging
import backoff
import requests

from config.meta import API_TOKEN

logger = logging.getLogger(__name__)


@backoff.on_exception(backoff.expo,
    (requests.exceptions.RequestException, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError,
     requests.exceptions.Timeout),
    max_tries=15,
    giveup=lambda e: e.response is not None and 400 <= e.response.status_code < 500)
def get(path: str, data: dict = None, timeout: int = 20) -> tuple[dict, int]:
    """
    Wrapper for requests.get, with default headers, timeouts and retries
    res = entry.get(f'/my/ships/{SHIP_ID}/navigate', data={'waypoint': 'X1-DF55-17335A'})
    """
    assert API_TOKEN is not None, 'API_TOKEN is not set'

    res = requests.get(
        f'https://api.spacetraders.io/v2{path}',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        },
        data=json.dumps(data) if data else None,
        timeout=timeout
    )

    res.raise_for_status()
    payload = res.json()
    return payload, res.status_code


@backoff.on_exception(backoff.expo,
    (requests.exceptions.RequestException, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError,
     requests.exceptions.Timeout),
    max_tries=15,
    giveup=lambda e: e.response is not None and 400 <= e.response.status_code < 500)
def post(path: str, data: dict = None, timeout: int = 20) -> tuple[dict, int]:
    """
    Wrapper for requests.post, with default headers, timeouts and retries
    """
    assert API_TOKEN is not None, 'API_TOKEN is not set'

    res = requests.post(
        f'https://api.spacetraders.io/v2{path}',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        },
        data=json.dumps(data) if data else None,
        timeout=timeout
    )

    try:
        res.raise_for_status()
        status_code = res.status_code
        payload = res.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code >= 500:
            logger.error(f'Error: {e}')
            logger.error(f'Payload: {e.response.json()}')
            raise e
        status_code = e.response.status_code
        payload = e.response.json()

    return payload, res.status_code
