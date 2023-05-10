import sys
sys.path.append('backend')

from backend.controllers import marketplace

def sell_goods():
    # Listing ship cargo
    print('Listing cargo...')
    cargos = marketplace.list_cargo()
    print(f'cargo: {cargos}')


    print('Docking ship...')
    assert marketplace.docking_ship(), 'Ship is not docked'

    print('Selling goods...')
    reciept = marketplace.sell_all_goods(cargos)
    print(reciept)
