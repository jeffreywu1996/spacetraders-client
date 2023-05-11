import pytest
import entry


def test_entry_get_my_agent():
    payload, status_code = entry.get('/my/agent')

    assert status_code == 200
    assert 'SUMMERRAINZ' in payload['data']['symbol']


def test_entry_get_list_cargo():
    payload, status_code = entry.get('/my/ships/SUMMERRAINZ-3')

    assert status_code == 200
    assert payload['data']['symbol'] == 'SUMMERRAINZ-3'
