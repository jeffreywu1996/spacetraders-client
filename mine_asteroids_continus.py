import time
import requests
from sell_goods import sell_goods

SHIP_ID = 'SUMMERRAINZ-2'

while True:
    print('Start mining...')
    try:
        res = requests.post(
            f'https://api.spacetraders.io/v2/my/ships/{SHIP_ID}/extract',
            headers={
                'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiU1VNTUVSUkFJTloiLCJpYXQiOjE2ODM2OTQzMDgsInN1YiI6ImFnZW50LXRva2VuIn0.OMq0ujeJI5n3jmEQd4-tP409vipu27l_edoe-hskWYk-HgfXP3uL2u5n530r3nDhqqJRXYaulyYdhDAPVvc-0DUHEXNUPKvJFewikvc9_oe98jM__V8TRWGWX6AoPEkQL2pWBx09PF5M1uqnVi15QIXq7ZzIQ9kavyURRBwDfoVhDQbV-WFGulwct_FCeVCUCTXXL9oU-lwzdSsjrXMdcRq-0g3e3oGr1O0VqvEE08uhs5e-kj9yF_LEnp1wbN-bHjbkFqpqK9H-xz-xBPpTKFmBoLHHh8pNC7mhmVWcOGnQAo-XIdWFktieiiZnrFNk50a-5B4ft_H1G7IoetXI8XZ3tHE0zYFxFN_Bh75lbomp9hQJ83aMJBUYWckQSKohdPXjLrZBpwzSiXO24iYIlXyaMJ_LaGcttFDNprjAxXA0zGDmoM1FzdeGs8Hv2mSpzCRMLGzXWdZdz0Wcev_TDmxjIEm89UYD_NCntUUGHIYEI1SRA7qsd2QIf1xOnYXC',
                'Content-Type': 'application/json'
            },
            timeout=5,
        )
    except requests.exceptions.Timeout:
        print('Timeout')
        time.sleep(2)
        continue

    payload = res.json()
    if res.status_code == 201:
        wait = payload['data']['cooldown']['remainingSeconds']
        print(f"Mining successful, wait {payload['data']['cooldown']['remainingSeconds']} seconds")
    elif res.status_code == 409:
        wait = payload['error']['data']['cooldown']['remainingSeconds']
        print(f"Mining in progrress. message: {payload['error']['message']}, wait: {payload['error']['data']['cooldown']['remainingSeconds']} seconds")
        time.sleep(wait)
        continue
    elif res.status_code == 400:
        print(f"Done mining")
        print(payload)
        # raise Exception(f'Mining done. message: {payload["error"]["message"]}')

        time.sleep(1)
        sell_goods()
        time.sleep(1)
    else:
        print(f'Unknown error. code = {res.status_code}')
        print(payload)
        raise Exception('Unknown error')

    if wait > 0:
        print(f'Waiting for {wait} seconds...')
        time.sleep(wait)
        print('done')

        try:
            print('Listing cargo...')
            res = requests.get(
                f'https://api.spacetraders.io/v2/my/ships/{SHIP_ID}',
                headers={
                    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiU1VNTUVSUkFJTloiLCJpYXQiOjE2ODM2OTQzMDgsInN1YiI6ImFnZW50LXRva2VuIn0.OMq0ujeJI5n3jmEQd4-tP409vipu27l_edoe-hskWYk-HgfXP3uL2u5n530r3nDhqqJRXYaulyYdhDAPVvc-0DUHEXNUPKvJFewikvc9_oe98jM__V8TRWGWX6AoPEkQL2pWBx09PF5M1uqnVi15QIXq7ZzIQ9kavyURRBwDfoVhDQbV-WFGulwct_FCeVCUCTXXL9oU-lwzdSsjrXMdcRq-0g3e3oGr1O0VqvEE08uhs5e-kj9yF_LEnp1wbN-bHjbkFqpqK9H-xz-xBPpTKFmBoLHHh8pNC7mhmVWcOGnQAo-XIdWFktieiiZnrFNk50a-5B4ft_H1G7IoetXI8XZ3tHE0zYFxFN_Bh75lbomp9hQJ83aMJBUYWckQSKohdPXjLrZBpwzSiXO24iYIlXyaMJ_LaGcttFDNprjAxXA0zGDmoM1FzdeGs8Hv2mSpzCRMLGzXWdZdz0Wcev_TDmxjIEm89UYD_NCntUUGHIYEI1SRA7qsd2QIf1xOnYXC',
                    'Content-Type': 'application/json'
                },
                timeout=5,
            )
        except requests.exceptions.Timeout:
            print('Timeout')
            time.sleep(2)
            continue

        payload = res.json()
        if res.status_code == 200:
            cargos = payload['data']['cargo']
            units = cargos['units']
            print(f'cargo units: {units}')
