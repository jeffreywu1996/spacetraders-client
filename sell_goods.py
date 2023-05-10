import json
import requests

SHIP_ID = 'SUMMERRAINZ-2'

# Listing ship cargo
print('Listing cargo...')
res = requests.get(
    f'https://api.spacetraders.io/v2/my/ships/{SHIP_ID}',
    headers={
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiU1VNTUVSUkFJTloiLCJpYXQiOjE2ODM2OTQzMDgsInN1YiI6ImFnZW50LXRva2VuIn0.OMq0ujeJI5n3jmEQd4-tP409vipu27l_edoe-hskWYk-HgfXP3uL2u5n530r3nDhqqJRXYaulyYdhDAPVvc-0DUHEXNUPKvJFewikvc9_oe98jM__V8TRWGWX6AoPEkQL2pWBx09PF5M1uqnVi15QIXq7ZzIQ9kavyURRBwDfoVhDQbV-WFGulwct_FCeVCUCTXXL9oU-lwzdSsjrXMdcRq-0g3e3oGr1O0VqvEE08uhs5e-kj9yF_LEnp1wbN-bHjbkFqpqK9H-xz-xBPpTKFmBoLHHh8pNC7mhmVWcOGnQAo-XIdWFktieiiZnrFNk50a-5B4ft_H1G7IoetXI8XZ3tHE0zYFxFN_Bh75lbomp9hQJ83aMJBUYWckQSKohdPXjLrZBpwzSiXO24iYIlXyaMJ_LaGcttFDNprjAxXA0zGDmoM1FzdeGs8Hv2mSpzCRMLGzXWdZdz0Wcev_TDmxjIEm89UYD_NCntUUGHIYEI1SRA7qsd2QIf1xOnYXC',
        'Content-Type': 'application/json'
    },
)
payload = res.json()
if res.status_code == 200:
    cargos = payload['data']['cargo']
    print(f'cargo: {cargos}')
    if cargos['units'] == 0:
        raise Exception('No cargo')
else:
    print(f'Unknown error. code = {res.status_code}')
    print(payload)


print('Docking ship...')
res = requests.post(
    f'https://api.spacetraders.io/v2/my/ships/{SHIP_ID}/dock',
    headers={
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiU1VNTUVSUkFJTloiLCJpYXQiOjE2ODM2OTQzMDgsInN1YiI6ImFnZW50LXRva2VuIn0.OMq0ujeJI5n3jmEQd4-tP409vipu27l_edoe-hskWYk-HgfXP3uL2u5n530r3nDhqqJRXYaulyYdhDAPVvc-0DUHEXNUPKvJFewikvc9_oe98jM__V8TRWGWX6AoPEkQL2pWBx09PF5M1uqnVi15QIXq7ZzIQ9kavyURRBwDfoVhDQbV-WFGulwct_FCeVCUCTXXL9oU-lwzdSsjrXMdcRq-0g3e3oGr1O0VqvEE08uhs5e-kj9yF_LEnp1wbN-bHjbkFqpqK9H-xz-xBPpTKFmBoLHHh8pNC7mhmVWcOGnQAo-XIdWFktieiiZnrFNk50a-5B4ft_H1G7IoetXI8XZ3tHE0zYFxFN_Bh75lbomp9hQJ83aMJBUYWckQSKohdPXjLrZBpwzSiXO24iYIlXyaMJ_LaGcttFDNprjAxXA0zGDmoM1FzdeGs8Hv2mSpzCRMLGzXWdZdz0Wcev_TDmxjIEm89UYD_NCntUUGHIYEI1SRA7qsd2QIf1xOnYXC',
        'Content-Type': 'application/json'
    },
)
if res.status_code != 200:
    print(f'Unknown error. code = {res.status_code}')
payload = res.json()
print(payload)
assert payload['data']['nav']['status'] == 'DOCKED'

print('Selling goods...')

for i in cargos['inventory']:
    data = {
        'symbol': i['symbol'],
        'units': i['units']
    }

    res = requests.post(
        f'https://api.spacetraders.io/v2/my/ships/{SHIP_ID}/sell',
        headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiU1VNTUVSUkFJTloiLCJpYXQiOjE2ODM2OTQzMDgsInN1YiI6ImFnZW50LXRva2VuIn0.OMq0ujeJI5n3jmEQd4-tP409vipu27l_edoe-hskWYk-HgfXP3uL2u5n530r3nDhqqJRXYaulyYdhDAPVvc-0DUHEXNUPKvJFewikvc9_oe98jM__V8TRWGWX6AoPEkQL2pWBx09PF5M1uqnVi15QIXq7ZzIQ9kavyURRBwDfoVhDQbV-WFGulwct_FCeVCUCTXXL9oU-lwzdSsjrXMdcRq-0g3e3oGr1O0VqvEE08uhs5e-kj9yF_LEnp1wbN-bHjbkFqpqK9H-xz-xBPpTKFmBoLHHh8pNC7mhmVWcOGnQAo-XIdWFktieiiZnrFNk50a-5B4ft_H1G7IoetXI8XZ3tHE0zYFxFN_Bh75lbomp9hQJ83aMJBUYWckQSKohdPXjLrZBpwzSiXO24iYIlXyaMJ_LaGcttFDNprjAxXA0zGDmoM1FzdeGs8Hv2mSpzCRMLGzXWdZdz0Wcev_TDmxjIEm89UYD_NCntUUGHIYEI1SRA7qsd2QIf1xOnYXC',
            'Content-Type': 'application/json'
        },
        data=json.dumps(data)
    )

    print(f'Sold goods, symbol: {data["symbol"]}, units: {data["units"]}, status_code: {res.status_code}')
