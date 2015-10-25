# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Get relevant libraries

# <codecell>

import ujson as json
import pprint
import pandas as pd
import numpy as np
import datetime
import fiona
import sklearn
import time
import datetime
import matplotlib.dates as mdates

from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from shapely.prepared import prep
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
from matplotlib import pyplot as plt
from sklearn.metrics.pairwise import pairwise_distances_argmin
from ggplot import *

%matplotlib inline

# <markdowncell>

# #Import data

# <codecell>

filename = "/Users/fnokeke/dev/student-streams/dataset/LocationHistory.json"

with open(filename) as json_file:
    raw = json.load(json_file)

ld = pd.DataFrame(raw['locations'])

print("Number of items in data: %d") % len(ld)

# <markdowncell>

# #Free up memory

# <codecell>

del raw

# <markdowncell>

# #Convert to typical units

# <codecell>

ld['latitudeE7'] = ld['latitudeE7']/float(1e7)
ld['longitudeE7'] = ld['longitudeE7']/float(1e7)
ld['timestampMs'] = ld['timestampMs'].map(lambda x: float(x)/1000)
ld['datetime'] = ld.timestampMs.map(datetime.datetime.fromtimestamp)
ld['dt2'] = ld.datetime.map(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
ld['date'] = ld.datetime.map(lambda x: x.strftime("%Y-%m-%d"))
ld['time'] = ld.datetime.map(lambda x: x.strftime("%H:%M:%S"))
ld['hr'] = ld.datetime.map(lambda x: x.strftime("%H"))
ld['min'] = ld.datetime.map(lambda x: x.strftime("%M"))

# <markdowncell>

# #Rename fields

# <codecell>

ld.rename(columns={
'latitudeE7': 'latitude',
'longitudeE7': 'longitude',
'timestampMs': 'timestamp'
}, inplace=True)

# <markdowncell>

# #Understand the data types of each column

# <codecell>

ld.dtypes

# <markdowncell>

# #Get a glimpse of raw data

# <codecell>

ld.head()

# <markdowncell>

# #Get only a specific number of weeks of data from specific start date

# <codecell>

no_of_weeks = 1
no_of_days = no_of_weeks * 7

start_date = ld[ld.date=='2014-11-09'].date.head(1)
start_date = pd.to_datetime(start_date)

print type(start_date)
dates = []
for i in range(no_of_days):
    x = (start_date + datetime.timedelta(days=-i)).to_string()[9:] # horrible tweak to get date in string format
    dates.append(x)
    
ld_wk = ld[ld.date.isin(dates)]
print "Week length:", len(ld_wk)
print dates[:5]

#type(pd.to_datetime("2014-11-09") + datetime.timedelta(days=-2))

# <markdowncell>

# #Ignore locations with accuracy estimates over 1000m

# <codecell>

ld_wk = ld_wk[ld_wk.accuracy < 1000]
ld_wk.reset_index(drop=True, inplace=True)
print("Number of items in data: %d") % len(ld_wk)

# <markdowncell>

# #Select only columns of interest

# <codecell>

ld_wk = ld_wk[['latitude', 'longitude', 'datetime', 'date']]

# <markdowncell>

# #Specify places of interest in Ithaca and ignore locations outside Ithaca

# <codecell>

home = (42.446594, -76.493736)
work = (42.444877, -76.480814)

lat_margin = 0.1
lon_margin = 1.0

ld_wk = ld_wk[abs(ld_wk.latitude - home[0]) < lat_margin]
ld_wk = ld_wk[abs(ld_wk.longitude - home[1]) < lon_margin]
print("Number of items in data: %d") % len(ld_wk)
ld_wk.head()
print "No of unique dates:", len(set(ld_wk.date))

# <markdowncell>

# #Label every location as either home, work or other

# <codecell>

lat_error_margin = 0.0005
lon_error_margin = 0.005

POINTS = {
    'home': home,
    'work': work
}

def get_loc_label(df, points):
    for label, point in points.items():
        within_lat = abs(df['latitude'] - point[0]) <= lat_error_margin
        within_lon = abs(df['longitude'] - point[1]) <= lon_error_margin
        if (within_lat and within_lon):
            return label
    else:
        return 'other'

ld_wk['loc_label'] = ld_wk.apply(lambda x: get_loc_label(x, POINTS), axis='columns')

# <markdowncell>

# #Show sample locations of home, work, other

# <codecell>

rows = [0,1,59,60,61,62]
ld_wk[ld_wk['date'] == ld_wk.date[0]].iloc[rows]

# <markdowncell>

# #Resample location patterns data by different time period

# <codecell>

loc_patterns = ld_wk[['datetime', 'loc_label']]
loc_patterns['freq'] = ld_wk['loc_label']
loc_patterns = loc_patterns.set_index('datetime')
loc_group = loc_patterns.groupby(['loc_label']).resample('6H',how=len)
loc_group = loc_group.reset_index()
loc_group.head()

# <codecell>

loc_group = loc_group.groupby(['datetime','loc_label']).sum()
loc_group.head()

# <codecell>

loc_group.unstack().head()

# <codecell>

loc_plot = loc_group.unstack().plot(kind='barh', stacked=True, title="Location Freq by Date", figsize=(15, 10))
loc_plot.set_xlabel("Frequency")
loc_plot.set_ylabel("Time")
loc_plot.legend(["Home","Other","Work"], loc=1,ncol=1)

# <codecell>


