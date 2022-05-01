import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px
from IPython.display import display
from folium.plugins import HeatMap
from folium import plugins, Map, Marker, features, Icon
from folium.plugins import HeatMap
import webbrowser
import os
from random import randint



# Clean Up Data

meteorites = pd.read_csv("./data/meteorite-landings.csv", delimiter=",")

# Rename columns
meteorites = meteorites.rename(columns={'name': 'Name', 'id': 'ID', 'nametype': 'Type', 'recclass': 'Class', 'mass': 'Mass', 'fall': 'Fell', 'year': 'Year', 'reclat': 'Latitude', 'reclong': 'Longitude'})

# Identify latitude and longitude columns (Assume latitude will be before longitude)
num_row = meteorites.shape[0]
num_col = meteorites.shape[1]
coord_col = []
for col_idx in range(num_col):
    temp = meteorites.iloc[: , col_idx] #create a view on column at index col_idx

    # check if most entries in column are likely to be int/float
    int_percent = 0
    num_tests = randint(100, 200)
    for test_num in range(num_tests): #test randomly on 100 to 200 entries in column being integers
        entry = temp[randint(100, num_row-100)] #pick any entry between index 100 index num_row-100 to avoid any padding in data
        if isinstance(entry, int) or isinstance(entry, float):
            int_percent += 1 #number of int/float entries
    int_percent = int_percent * 100 / num_tests # convert to percentage: percent of tests which were int/float

    if int_percent > 90:
        f_temp = temp[(temp >= -180) & (temp <= 180)]
        
        # If more than 80% values are in our coordinates range
        if f_temp.shape[0] * 100/num_row > 80:
            if len(coord_col) < 2:
                coord_col.append(col_idx)

# print(f"-----------------------COLS {coord_col}-----------------------")
# lat = meteorites.columns[col_idx[0]]
# lon = meteorites.columns[col_idx[1]]
# meteorites = meteorites.rename(columns={lat: 'Latitude', lon: 'Longitude'})

# meteorites = meteorites.rename(columns={meteorites.columns[col_idx[0]]: 'Latitude', meteorites.columns[col_idx[1]]: 'Longitude'})
# meteorites.columns.values[col_idx[0]] = "Latitude"
# meteorites.columns.values[col_idx[1]] = "Longitude"
# mapping = {meteorites.columns[col_idx[0]]: 'Latitude', meteorites.columns[col_idx[1]]: 'Longitude'}
# meteorites = meteorites.rename(columns=mapping)


# Get rid of faulty datapoints (dataset specific)
filtered_coords = (meteorites["Longitude"] >= -180) & (meteorites["Longitude"] <= 180) & ((meteorites["Longitude"] != 0) | (meteorites["Latitude"] != 0))
filtered_years = (meteorites["Year"] >= 860) & (meteorites["Year"] <= 2016)
filtered_mass = ~pd.isna(meteorites["Mass"])
filtered_type = ((meteorites["Type"] == "Valid"))
filtered_meteorites = meteorites[filtered_coords & filtered_years & filtered_type & filtered_mass]
filtered_meteorites.drop(["GeoLocation", "Type"], axis=1, inplace=True)
filtered_meteorites["Mass"] = filtered_meteorites["Mass"].div(1000) # convert gram to kilogram
filtered_meteorites.to_csv("./data/cleansed-data.csv")
filtered_meteorites = filtered_meteorites.sort_values(by="Year", ascending=True)

# open cleansed data file
cleansed_meteorites = pd.read_csv("./data/cleansed-data.csv", delimiter=",")

# input: time period for heatmap and minimum mass of meteorite for plot points
start_year = int(input("Input start year: "))
end_year = int(input("Input end year: "))
min_mass = int(input("Minimum mass of meteorite points to plot (in kg): "))

# create view on dataframe (in inputted time span)
mask1 = (cleansed_meteorites["Year"] >= start_year) & (cleansed_meteorites["Year"] <= end_year) & (cleansed_meteorites["Mass"] >= min_mass)
mask2 = (cleansed_meteorites["Year"] >= start_year) & (cleansed_meteorites["Year"] <= end_year)
include = cleansed_meteorites[mask1]

# updated mask for heatmap
mask2 = cleansed_meteorites[mask2]


map = Map(location=[0, 0], zoom_start=2, control_scale=True)


# plot points using mask1
for index, row in include.iterrows():
    icon = features.CustomIcon("https://i.imgur.com/YCwSiQa.png", icon_size=(53.75,66.25)) # custom icon
    Marker([row["Latitude"], row["Longitude"]],
    popup = "Name: " + row["Name"] + " Mass: " + str(row["Mass"]) + " Fall: " + str(row["Fell"]) + " Lat: " + str(row["Latitude"]) + " Long: " + str(row["Longitude"]),
    icon=icon ).add_to(map)

# plot heatmap using mask2
mask2 = mask2[['Latitude', 'Longitude']]
# mask = mask.dropna(axis=0, subset=['Latitude','Longitude'])
map_data = [[row['Latitude'],row['Longitude']] for index, row in mask2.iterrows()]
HeatMap(map_data).add_to(map)

# save map as html file and open in browser
map.save("map.html")
webbrowser.open("map.html")
webbrowser.open('file://' + os.path.realpath("map.html")) # open file in default browser
