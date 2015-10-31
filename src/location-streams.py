
# coding: utf-8

# # Get relevant libraries

<<<<<<< HEAD
# In[299]:
=======
# In[117]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

import ujson as json
import pprint
import pandas as pd
import numpy as np
import datetime
import time
import datetime
import calendar
import seaborn as sns

import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from ggplot import *

<<<<<<< HEAD

# # All plots should be inside notebook

# In[300]:

=======
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a
get_ipython().magic(u'matplotlib inline')
pd.options.mode.chained_assignment = None  # remove default='warn'


# # Import data

<<<<<<< HEAD
# In[301]:
=======
# In[29]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

filename = "/Users/fnokeke/dev/student-streams/dataset/LocationHistory.json"
with open(filename) as json_file:
    raw = json.load(json_file)

ld = pd.DataFrame(raw['locations'])
print("Number of items in data: %d") % len(ld)

<<<<<<< HEAD
# free up memory
=======

# #Free up memory

# In[30]:

>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a
del raw


# # Convert to typical units and rename columns

<<<<<<< HEAD
# In[303]:
=======
# In[31]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

ld['latitudeE7'] = ld['latitudeE7']/float(1e7)
ld['longitudeE7'] = ld['longitudeE7']/float(1e7)
ld['timestampMs'] = ld['timestampMs'].map(lambda x: float(x)/1000)
ld['datetime'] = ld.timestampMs.map(datetime.datetime.fromtimestamp)
<<<<<<< HEAD
ld['date'] = ld.datetime.map(lambda x: x.strftime("%Y-%m-%d")) # TODO: remove
=======
ld['dt2'] = ld.datetime.map(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
ld['date'] = ld.datetime.map(lambda x: x.strftime("%Y-%m-%d"))
ld['time'] = ld.datetime.map(lambda x: x.strftime("%H:%M:%S"))
ld['hr'] = ld.datetime.map(lambda x: x.strftime("%H"))
ld['min'] = ld.datetime.map(lambda x: x.strftime("%M"))


# #Rename fields

# In[32]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

ld.rename(columns={
'latitudeE7': 'latitude',
'longitudeE7': 'longitude',
'timestampMs': 'timestamp'
}, inplace=True)

<<<<<<< HEAD

# # Glimpse of raw data
=======

# #Understand the data types of each column

# In[33]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

# In[336]:

<<<<<<< HEAD
print ld.dtypes
ld.head()
=======
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a


<<<<<<< HEAD
# # Get only a specific number of weeks of data from specific start date
=======
# In[54]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

# In[337]:

<<<<<<< HEAD
no_of_weeks = 1
no_of_days = no_of_weeks * 7
=======
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a


<<<<<<< HEAD
# # Get date in string format
=======
# In[55]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

# In[338]:

start_date = ld[ld.date=='2014-11-09'].date.head(1)
start_date = pd.to_datetime(start_date)

dates = []
for i in range(no_of_days):
    x = (start_date + datetime.timedelta(days=-i)).to_string()[9:] # horrible tweak to get date in string format
    dates.append(x)
    
ld_wk = ld[ld.date.isin(dates)]
print "Week length:", len(ld_wk)
print dates[:5]

<<<<<<< HEAD
=======
# type(pd.to_datetime("2014-11-09") + datetime.timedelta(days=-2))

>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

# # Ignore locations with accuracy estimates over 1000m

<<<<<<< HEAD
# In[339]:
=======
# In[56]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

ld_wk = ld_wk[ld_wk.accuracy < 1000]
ld_wk.reset_index(drop=True, inplace=True)
print("Number of items in data: %d") % len(ld_wk)


# # Select only columns of interest

<<<<<<< HEAD
# In[340]:
=======
# In[57]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

ld_wk = ld_wk[['latitude', 'longitude', 'datetime', 'date']]


# # Specify places of interest in Ithaca and ignore locations outside Ithaca

<<<<<<< HEAD
# In[341]:
=======
# In[58]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

home = (42.446594, -76.493736)
work = (42.444877, -76.480814)

lat_margin = 0.1
lon_margin = 1.0

ld_wk = ld_wk[abs(ld_wk.latitude - home[0]) < lat_margin]
ld_wk = ld_wk[abs(ld_wk.longitude - home[1]) < lon_margin]
print("Number of items in data: %d") % len(ld_wk)
ld_wk.head()
print "No of unique dates:", len(set(ld_wk.date))


# # Label every location as either home, work or other

<<<<<<< HEAD
# In[342]:
=======
# In[59]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

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


# # Show sample locations of home, work, other

<<<<<<< HEAD
# In[343]:
=======
# In[60]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

rows = [0,1,59,60,61,62]
ld_wk[ld_wk['date'] == ld_wk.date[0]].iloc[rows]


# # Resample location patterns data by different time period

<<<<<<< HEAD
# In[344]:
=======
# In[61]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

loc_patterns = ld_wk[['datetime', 'loc_label']]
loc_patterns = loc_patterns.set_index('datetime')
loc_patterns['freq'] = 0
loc_group = loc_patterns.groupby(['loc_label']).resample('6H',how=len)
loc_group = loc_group.reset_index()
loc_group.head()


<<<<<<< HEAD
# In[345]:
=======
# In[62]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

loc_group = loc_group.groupby(['datetime','loc_label']).sum()
loc_group.head()


<<<<<<< HEAD
# In[346]:

loc_group.unstack().head()

=======
# In[63]:

loc_group.unstack().head()


# In[64]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

# In[754]:

loc_plot = loc_group.unstack().plot(kind='barh', stacked=True, title="Location Freq by Date", figsize=(10,5))
loc_plot.set_xlabel("Frequency")
loc_plot.set_ylabel("Time")
r = loc_plot.legend(["Home","Other","Work"],loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)


# # Mark every day by the day name

<<<<<<< HEAD
# In[674]:
=======
# In[65]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

weekday_patterns = ld_wk[['datetime', 'loc_label']]
weekday_patterns['weekday'] = weekday_patterns.datetime.map(lambda x: calendar.day_name[x.weekday()])
weekday_patterns['day'] = weekday_patterns.datetime.map(lambda x: x.weekday())
weekday_patterns.head()

<<<<<<< HEAD
=======

# In[66]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

# # ggplot of day_of_week vs location frequency (stacked bar)

<<<<<<< HEAD
# In[556]:
=======

# In[67]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

weekday_label = ("Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun")

<<<<<<< HEAD
ggplot(weekday_patterns, aes("day", fill='loc_label')) + geom_bar() +     scale_x_continuous(name="Day of Week", labels=weekday_label) +     scale_y_continuous(name="Frequency", labels="comma") +     ggtitle("Location Frequency by Day of Week") +     theme_seaborn()
=======

# In[68]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a


<<<<<<< HEAD
# # ggplot of day_of_week vs location frequency (multiple lines)
=======

# In[69]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

# In[612]:

<<<<<<< HEAD
wkdf = weekday_patterns[['day', 'loc_label']]
wkdf['freq'] = 0
wkdf = wkdf.groupby(['day', 'loc_label']).count().reset_index()
=======

# In[70]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

ggplot(wkdf, aes('day', 'freq', color='loc_label')) + geom_line() +     scale_x_continuous(name="Day of Week", labels=weekday_label) +     scale_y_continuous(name="Frequency", labels="comma") +     ggtitle("Location Frequency by Day of Week") +     theme_seaborn()


# # Show location frequency by date (ggplot)

<<<<<<< HEAD
# In[753]:
=======
# In[208]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

date_df = weekday_patterns[['datetime', 'loc_label']]
date_df['freq'] = 0

date_df = date_df.set_index('datetime')
date_df = date_df.groupby('loc_label').resample('D', how='count').reset_index()

ggplot(date_df, aes('datetime', 'freq', color='loc_label')) +     geom_line() +     scale_x_date(name="Date", labels="%b %d %-I %p", breaks=date_breaks("8 hours")) +     ggtitle("Frequency of Location by Time") +     theme_bw()


# # Datetime by barchart (ggplot)

<<<<<<< HEAD
# In[728]:

date_df = weekday_patterns[['datetime', 'loc_label']]
date_df['freq'] = 0

pp = date_df.set_index('datetime').groupby('loc_label').resample('D', how='count').reset_index()
pp
=======

# In[209]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a


<<<<<<< HEAD
# In[739]:
=======
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

qq=pd.melt(pp, id_vars=['datetime','loc_label'])
qq['x'] = qq.index
qq.head(10)

<<<<<<< HEAD
=======
# In[210]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

# In[744]:

ggplot(qq, aes('x', weight='value', fill='loc_label')) +     geom_bar() +     ggtitle("Frequency of Location by Time")


# # Resample dates by specific period (hours, days, weeks)

<<<<<<< HEAD
# In[349]:

weekday_patterns['freq'] = 0
weekday_patterns = weekday_patterns.set_index('datetime')
weekday_patterns = weekday_patterns.groupby(['weekday', 'loc_label']).resample('D', how=len)
weekday_patterns.head()


# # Where you are by dates

# In[393]:

day_time_patterns = ld_wk[['datetime', 'loc_label']]

day_time_patterns['hr'] = day_time_patterns.datetime.map(lambda x: int(x.strftime("%H")) + float(x.strftime("%M"))/60)
day_time_patterns.hr = pd.Categorical(day_time_patterns.hr)
day_time_patterns.hr = day_time_patterns.hr.astype(float)

# TODO: remove this weekday code if already using day_value
day_time_patterns['weekday'] = day_time_patterns.datetime.map(lambda x: calendar.day_name[x.weekday()])
day_time_patterns.weekday = pd.Categorical(day_time_patterns.weekday, order_of_weekdays)

day_time_patterns.loc_label = pd.Categorical(day_time_patterns.loc_label)
day_time_patterns.head()


# # Show location by time of day (seaborn plot)

# In[394]:
=======

# In[211]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

def get_day_num(day): 
    if day == 'Monday':
        return 1
    elif day == 'Tuesday':
        return 2    
    elif day == 'Wednesday':
        return 3    
    elif day == 'Thursday':
        return 4    
    elif day == 'Friday':
        return 5    
    elif day == 'Saturday':
        return 6    
    elif day == 'Sunday':
        return 7

day_time_patterns['day_value'] = day_time_patterns.weekday.astype(str).map(lambda x: get_day_num(x))


<<<<<<< HEAD
# In[608]:
=======
# In[214]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

day_time_patterns.rename(columns={'loc_label': 'Location'}, inplace=True)
day_time_patterns.head()


<<<<<<< HEAD
# # Day of week by time of day for location

# In[716]:
=======

# In[269]:
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a

weekday_label = ("Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun")
time_label = ("Midnight", "5am", "10am", "3pm", "8pm", "Midnight")

ggplot(day_time_patterns, aes('day_value', 'hr', color='Location')) +     geom_point() +     scale_x_continuous(name = "Day of Week", breaks=range(1,8), labels=weekday_label) +     scale_y_continuous(name="Time of Day", limits=(0,25), labels=time_label)


<<<<<<< HEAD
# In[764]:

meat = meat.dropna(thresh=800, axis=1) # drop columns that have fewer than 800 observations
ts = meat.set_index(['date'])
ts.head(10)


# In[765]:

ts.groupby(ts.index.year).sum().head(10)


=======
>>>>>>> 1ca28dde6d6e88117cf380c313ac9af30eeb2e5a
# In[ ]:



