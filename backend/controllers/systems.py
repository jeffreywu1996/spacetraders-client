import logging
from functools import cache

import entry


logger = logging.getLogger(__name__)



@cache
def list(type=None) -> dict:
    """
    returns {'waypoints': [{
        'type': 'PLANET',
        'symbol': 'X1-DF55-20250Z',
        'x': 0,
        'y': 0,
    }]}
    """
    payload, status_code = entry.get(f'/systems')

    # if type:
    #     waypoints = [w for w in waypoints if w['type'] == type]

    # return {'waypoints': waypoints}, status_code
    return payload, status_code

@cache
def get_system_names():
    payload, status_code = entry.get(f'/systems')
    systems = [w['symbol'] for w in payload['data']]
    return systems, status_code

@cache
def get_systems(system=None):
    payload, status_code = entry.get(f'/systems')
    if system:
        systems = [w for w in payload['data'] if w['symbol'] == system]
    else:
        systems = [w for w in payload['data']]
    return systems, status_code


@cache
def list_waypoints(system):
    payload, status_code = entry.get(f'/systems/{system}/waypoints')
    # waypoints = [w['symbol'] for w in payload['data']['waypoints']]
    return payload['data'], status_code


@cache
def get_waypoint(system, waypoint):
    payload, status_code = entry.get(f'/systems/{system}/waypoints/{waypoint}')
    return payload['data'], status_code

@cache
def get_waypoint_names(system):
    payload, status_code = entry.get(f'/systems/{system}/waypoints')
    systems = [w['symbol'] for w in payload['data']]
    return systems, status_code


@cache
def get_shipyard(system, waypoint):
    payload, status_code = entry.get(f'/systems/{system}/waypoints/{waypoint}/shipyard')
    return payload['data'], status_code
