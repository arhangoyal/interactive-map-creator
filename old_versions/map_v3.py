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
from myfunctions import find_coordinate_cols, clean_coord_data



# main

infile = input("Enter full/relative path to (CSV) dataset on system: ") # "./input/meteorite-landings.csv"
find_coordinate_cols(infile)
clean_coord_data("./data/coord-data-found.csv")



# Plot data

# open coordinate filtered data file
clean_df = pd.read_csv("./data/coord-filtered-data.csv", delimiter=",")
clean_df["mass"] = clean_df["mass"].div(1000) # convert gram to kilogram

# input: time period for heatmap and minimum mass of meteorite for plot points
start_year = int(input("Input start year: "))
end_year = int(input("Input end year: "))
min_mass = int(input("Minimum mass of meteorite points to plot (in kg): "))

# create view on dataframe (in inputted time span)
mask1 = (clean_df["year"] >= start_year) & (clean_df["year"] <= end_year) & (clean_df["mass"] >= min_mass)
mask2 = (clean_df["year"] >= start_year) & (clean_df["year"] <= end_year)
include = clean_df[mask1]

# updated mask for heatmap
mask2 = clean_df[mask2]


map = Map(location=[0, 0], zoom_start=2, control_scale=True)


# plot points using mask1
for index, row in include.iterrows():
    icon = features.CustomIcon("https://i.imgur.com/YCwSiQa.png", icon_size=(53.75,66.25)) # custom icon
    Marker([row["Latitude"], row["Longitude"]],
    popup = "Name: " + row["name"] + " Mass: " + str(row["mass"]) + " Fall: " + str(row["fall"]) + " Lat: " + str(row["Latitude"]) + " Long: " + str(row["Longitude"]),
    icon=icon ).add_to(map)

# plot heatmap using mask2
mask2 = mask2[['Latitude', 'Longitude']]
map_data = [[row['Latitude'],row['Longitude']] for index, row in mask2.iterrows()]
HeatMap(map_data).add_to(map)

# save map as html file and open in browser
map.save("./output/map.html")
webbrowser.open('file://' + os.path.realpath("./output/map.html")) # open file in default browser
