import pandas as pd
import numpy as np

import geopandas as gpd   

from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

path = '/Users/sbuenker/neuefische/florita/'
#counties = gpd.read_file(path + 'data/geo/county/cb_2018_us_county_5m.shp')
claims_by_year = pd.read_csv(path +'data/claims_by_year.csv')
agg_total = pd.read_csv(path +'data/agg_total_df.csv', dtype={'countyCode': 'str'})