import logging

import entry


logger = logging.getLogger(__name__)


def agent():
    payload, status_code = entry.get(f'/my/agent')
    return payload, status_code


def credits():
    payload, status_code = entry.get(f'/my/agent')
    return payload['data']['credits'], status_code
