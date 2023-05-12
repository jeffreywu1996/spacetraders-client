import os
from dotenv import dotenv_values


SHIP_ID = os.getenv('SHIP_ID', 'SUMMERRAINZ-2')
API_TOKEN = dotenv_values('.env').get('API_TOKEN')
CONTRACT_ID = 'clhh84b2c17vss60d6okrr8yo'
