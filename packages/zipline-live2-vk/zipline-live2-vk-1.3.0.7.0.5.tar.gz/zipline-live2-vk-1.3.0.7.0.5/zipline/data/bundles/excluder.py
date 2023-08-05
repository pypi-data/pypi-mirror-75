"""
IB TWS sometimes does not recognize sumbols provided by quandl/sharadar. It is painful experience
when your pipeline crashes due to this reason. In order to overcome this we run exclude routine from
this file which creates local copy (pickle file) of the list containing the exclusions. These exclusions
file is then treated in a due way by sharadar-ext insgest module (see sharadar_ext.py).

However in order to run the excluder you have to have already the copy of sharadar-ext (or whatever
bundle you use) on your local machine. So the proper sequence of actions should be:
1) ingest your bundle to your local machine if you don't have any (zipline just installed)
2) run exclude('your bundle')
3) ingest your bundle once again.
"""

from zipline.data import bundles
from zipline.gens.brokers.ib_broker2 import IBBroker
import pandas as pd
from datetime import datetime
import pytz
import pickle
from zipline.data.bundles.sharadar_ext import EXCLUSIONS_FILE


def exclude(bundle='sharadar-ext'):
    tws_uri = 'localhost:7496:1'
    broker = IBBroker(tws_uri)

    bundle_data = bundles.load(
        bundle,
    )

    all_sids = bundle_data.asset_finder.sids
    all_assets = bundle_data.asset_finder.retrieve_all(all_sids)

    exclusions = []

    for i, asset in enumerate(all_assets):
        live_today = pd.Timestamp(datetime.utcnow().date()).replace(tzinfo=pytz.UTC)
        if asset.to_dict()['end_date'] + pd.offsets.BDay(1) >= live_today:
            print(f'Checking {asset.symbol} symbol')
            contracts = broker.reqMatchingSymbols(asset.symbol)
            if asset.symbol not in [c.contract.symbol for c in contracts]:
                print(f'!!!No IB data for {asset.symbol}!!!')
                exclusions.append(asset.symbol)
        else:
            print(f'Skipping check for {asset.symbol} as it is not traded any more')

    with open(EXCLUSIONS_FILE, 'wb') as f:
        pickle.dump(exclusions, f)

    print(f'{len(exclusions)} exclusions found!')