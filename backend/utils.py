import dateutil.parser
from datetime import datetime


def get_timestamp_in_ms():
    return int(datetime.now().timestamp() * 1000)


def get_timestamp_in_sec():
    return int(datetime.now().timestamp())


def secs_until_iso_date(iso_str):
    """
    Returns the number of seconds until the iso_str date
    """
    # secs = datetime.fromisoformat(iso_str).timestamp() - get_timestamp_in_sec()
    secs = dateutil.parser.isoparse(iso_str).timestamp() - get_timestamp_in_sec()

    if secs < 0:
        raise ValueError(f'iso_str: {iso_str} is in the past!')

    return secs
