import sys
sys.path.append('backend')

import streamlit as st # web development
import numpy as np # np mean, np random
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop
import plotly.express as px # interactive charts
import uuid
from datetime import datetime

from backend.controllers import agent
from backend.controllers import systems
from backend.controllers import contract
from backend.controllers import marketplace


SHIP = 'SUMMERRAINZ-A'
SYSTEM = 'X1-DF55'
ASTEROID_FIELD = 'X1-DF55-17335A'
QUEST_LOCATION = 'X1-DF55-20250Z'
CONTRACT_ID = 'clhh84b2c17vss60d6okrr8yo'

ORE_TO_MINE = 'ALUMINUM_ORE'
MINE_UNITS = 60


st.set_page_config(
    page_title = 'SpaceTraders Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

st.title("SpaceTraders Dashboard")


# creating a single-element container.
placeholder = st.empty()

# dataframe filter
market_df = pd.DataFrame({
    'time': [],
    'symbol': [],
    'tradeVolume': [],
    'supply': [],
    'purchasePrice': [],
    'sellPrice': [],
})


price_data = {}

for seconds in range(200):
#while True:
    with placeholder.container():

        credits, contracts = st.columns(2)
        # payload, status_code = marketplace.get_prices('X1-DF55', 'X1-DF55-17335A', 'ALUMINUM_ORE')
        payload, status_code = agent.credits()
        credits.markdown("## Credits")
        credits.metric(label="Credits", value=payload)

        payload, status_code = contract.list()
        contracts.markdown("## Credits")
        contracts.json(payload['data'])


        st.markdown("## Systems")
        # systems_filter = st.selectbox("Select a System", systems.get_system_names()[0], key=uuid.uuid4())
        systems_filter = st.selectbox("Select a System", systems.get_system_names()[0])

        _systems, status_code = systems.get_systems(system=systems_filter)
        st.markdown('### System')
        _systems = _systems[0]
        st.json({x: _systems[x] for x in _systems if x not in ['waypoints']})

        st.markdown('### Waypoints')
        waypoints, status_code = systems.list_waypoints(system=systems_filter)
        first, second = st.columns(2)
        # st.json(payload)
        for ind, w in enumerate(waypoints):
            if ind % 2 == 0:
                first.markdown(f'##### {w["symbol"]}: {w["type"]}')
                first.json(w)
            else:
                second.markdown(f'##### {w["symbol"]}: {w["type"]}')
                second.json(w)
        # st.json(payload[0])

        st.markdown("## Shipyard")
        has_shipyards = [w for w in waypoints if any(t['symbol'] == 'SHIPYARD' for t in w['traits'])]
        st.metric(label="Waypoints with shipyard", value=str([w['symbol'] for w in has_shipyards]))
        waypoint_names, _ = systems.get_waypoint_names(systems_filter)
        filtered_waypoints = [w for w in waypoint_names if w in [w['symbol'] for w in has_shipyards]]
        shipyard_waypoint_filter = st.selectbox("Select a Waypoint", filtered_waypoints)
        # st.metric(label="Selected waypoint", value=waypoint_filter)
        shipyards = systems.get_shipyard(system=systems_filter, waypoint=shipyard_waypoint_filter)
        st.json(shipyards)


        st.markdown("## Marketplace")
        # payload, _ = marketplace.get_prices(SYSTEM, ASTEROID_FIELD, ORE_TO_MINE)
        # market_df.loc[len(market_df.index)] = [str(datetime.now().isoformat()) , payload['symbol'], payload['tradeVolume'], payload['supply'], payload['purchasePrice'], payload['sellPrice']]
        # st.dataframe(market_df)
        has_marketplace = [w for w in waypoints if any(t['symbol'] == 'MARKETPLACE' for t in w['traits'])]
        has_marketplace_names = [w['symbol'] for w in has_marketplace]
        st.metric(label="Waypoints with marketplace", value=str(has_marketplace_names))
        marketplace_waypoint_filter = st.selectbox("Select a Waypoint", has_marketplace_names)
        payload, _ = marketplace.get_prices(systems_filter, marketplace_waypoint_filter, 'ALUMINUM_ORE')
        st.json(payload)

        # st.markdown("### Detailed Data View")
        # st.dataframe(df)
        time.sleep(60)
    #placeholder.empty()
