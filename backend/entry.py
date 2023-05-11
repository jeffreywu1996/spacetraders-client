import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from config.meta import API_TOKEN


def get(path: str, data: dict = None, timeout: int = 10) -> tuple[dict, int]:
    """
    Wrapper for requests.get, with default headers, timeouts and retries
    res = entry.get(f'/my/ships/{SHIP_ID}/navigate', data={'waypoint': 'X1-DF55-17335A'})
    """
    s = requests.Session()
    retries = Retry(
        total=5, backoff_factor=1, backoff_jitter=5,
        status_forcelist=[ 502, 503, 504 ]
    )
    s.mount('http://', HTTPAdapter(max_retries=retries))

    res = s.get(
        f'https://api.spacetraders.io/v2{path}',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        },
        data=json.dumps(data) if data else None,
        # timeout=timeout
    )

    res.raise_for_status()
    payload = res.json()
    return payload, res.status_code
