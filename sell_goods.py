import sys
sys.path.append('backend')

from backend.controllers import marketplace

SHIP_ID = 'SUMMERRAINZ-2'

# Listing ship cargo
print('Listing cargo...')
cargos = marketplace.list_cargo()
print(f'cargo: {cargos}')


print('Docking ship...')
assert marketplace.docking_ship(), 'Ship is not docked'

print('Selling goods...')
reciept = marketplace.sell_all_goods(cargos)
print(reciept)
