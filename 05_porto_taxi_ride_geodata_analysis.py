#!/usr/bin/env python
# coding: utf-8

# In[1]:


import folium
import pandas as pd 
import datetime, calendar


# In[2]:


df = pd.read_csv("data/porto_taxi_ride.csv")
df.head()


# ######
# CALL_TYPE : The way used to demand taxi service
# 1. 'A': If it is dispatched frm the Central
# 2. 'B': If the trip was demanded directly to a taxi driver on a specific stand
# 3. 'C': Other
# 
# TIMESTAMP: When the strip starts
# TRIP_PATH: Contains a list of co-ordinates
# 1. The first element is the co-ordinates of the trip starting point
# 2. Last element is the co-ordinates of the trip ending point

# DATA Pre-Processing

# ###### Creating two columns as ``START_LOC`` and ``END_LOC``

# In[3]:


#to convert strings to list
df.TRIP_PATH = df.TRIP_PATH.apply(eval)
df.head()


# In[4]:


extract_starting_point = lambda list_ : list_ [0]
extract_ending_point = lambda list_ : list_ [-1]

df["START_LOC"] = df.TRIP_PATH.apply(extract_ending_point)
df["END_LOC"] = df.TRIP_PATH.apply(extract_ending_point)


# In[5]:


df.head()


# In[6]:


#Remapping ``CALL_TYPE`` column values to the proper values

CALL_TYPES = {
    "A":"CENTRAL_BASED",
    "B":"STAND_BASED",
    "C":"OTHER"
}
df.CALL_TYPE = df.CALL_TYPE.map(CALL_TYPES)
df.head()


# In[7]:


#number of counts for each way to get a taxi in Porto
df.CALL_TYPE.value_counts()


# In[8]:


d1 = df.CALL_TYPE.value_counts()
d1.plot.bar(grid=True)


# ### Which regions of the city are the best pick up points

# In[9]:


map = folium.Map(location=[41.15, -8.62], zoom_start=16)

for point in df.START_LOC:
    folium.CircleMarker(location=point, color = "red",radius = 1, weight = 3).add_to(map)

map


# ### Which regions of the city are the best pick up points for stand-based trips

# In[10]:


smap = folium.Map(location=[41.15,-8.62], zoom_start=16)

colors = {
    "OTHER":"green",
    "STAND_BASED": "red",
    "CENTRAL_BASED": "blue"
}
smap_df = df[["CALL_TYPE","START_LOC"]]

for index, row in smap_df.iterrows():
    color = colors[row["CALL_TYPE"]]
    location = row["START_LOC"]
    folium.CircleMarker(location, color=color,radius=1, weight=2).add_to(smap)

smap


# ###  Which regions of the city are the most common destination on Mondays

# In[11]:


list(calendar.day_name)


# In[12]:


day_names = list(calendar.day_name)


# In[13]:


get_day = lambda timestamp : day_names[datetime.datetime.fromtimestamp(timestamp).weekday()]
df["Week_day"] = df.TIMESTAMP.apply(get_day)
df.head()


# In[14]:


#getting all the trips on Mondays
monday_df = df[df.Week_day == "Monday"]
monday_df.head()


# In[15]:


mon_map = folium.Map(location=[41.15,-8.62], zoom_start=16)

for loc in monday_df.END_LOC:
    folium.CircleMarker(loc, color='red',radius=1, weight=2).add_to(mon_map)
mon_map


# ### Common Destination on Monday mornings between 6 & 9

# In[16]:


extract_hour = lambda timestamp : datetime.datetime.fromtimestamp(timestamp).hour
df["Hours"] = df.TIMESTAMP.apply(extract_hour)
df


# In[17]:


monhour_df = df[(df.Week_day == "Monday") & ((df.Hours >6 ) & (df.Hours <9))]
monhour_df.head()


# In[18]:


qmap = folium.Map(location=[41.15,-8.62],zoom_start=14)
start_loc = lambda loc : folium.CircleMarker(loc, color="red",radius=1,weight=2).add_to(qmap)
end_loc = lambda loc : folium.CircleMarker(loc, color='blue',radius=1,weight=2).add_to(qmap)

monhour_df.START_LOC.apply(start_loc)
monhour_df.END_LOC.apply(end_loc)
qmap


# ### Analyzing rush hour in the city of Porto - The most busiest streets

# In[19]:


df.head()


# In[20]:


df.Hours.value_counts()


# In[21]:


df.Hours.value_counts().sort_index().plot.bar()


# which street has the most traffic during the rush hour

# In[22]:


qdf = df[df.Hours == 13]
qdf.head()


# In[23]:


qmap1 = folium.Map(location=[41.15,-8.62], zoom_start=14)

for coords in qdf.TRIP_PATH:
    folium.PolyLine(coords, color="red",opacity= 0.1,weight=2).add_to(qmap1)
qmap1


# In[ ]:




