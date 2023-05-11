from config.meta import SHIP_ID, API_TOKEN


def test_api_token_exists():
    assert API_TOKEN is not None


def test_ship_id_exists():
    assert SHIP_ID is not None
