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



# Clean Up Data

meteorites = pd.read_csv("./data/meteorite-landings.csv", delimiter=",")
# Rename columns
meteorites = meteorites.rename(columns={'name': 'Name', 'id': 'ID', 'nametype': 'Type', 'recclass': 'Class', 'mass': 'Mass', 'fall': 'Fell', 'year': 'Year', 'reclat': 'Latitude', 'reclong': 'Longitude'})
# Get rid of faulty datapoints
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
