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

# myfunctions.py contains the functions I have written for the interactive map creator
from myfunctions import find_coordinate_cols, clean_coord_data, get_map_filter



# main

infile = input("Enter full/relative path to (CSV) dataset on system: ") # ./input/meteorite-landings.csv

# clean data (meteorite data specific)
dirty_df = pd.read_csv(infile, delimiter=",")
filtered_mass = ~pd.isna(dirty_df["mass"])
filtered_type = ((dirty_df["nametype"] == "Valid"))
dirty_df = dirty_df[filtered_mass & filtered_type]
dirty_df.drop(["GeoLocation", "nametype"], axis=1, inplace=True)
dirty_df = dirty_df.sort_values(by="year", ascending=True)
dirty_df["mass"] = dirty_df["mass"].div(1000) # convert gram to kilogram. This is specific to the meteorite dataset
dirty_df.to_csv("./data/pre-cleaned-data.csv", index=False)

# Find coordinate columns, rename them, and filter out data outside valid coordinate range
find_coordinate_cols("./data/pre-cleaned-data.csv")
clean_coord_data("./data/coord-data-found.csv")


# Plot data

# open coordinate filtered data file
clean_df = pd.read_csv("./data/coord-filtered-data.csv", delimiter=",")

# input: filter 1 (col1) for heatmap and plot points and filter 2 (col2) for plot points only
col1, col1_min, col1_max = get_map_filter(clean_df, "Enter name of column 1 (int/float) to filter out data: ")
col2, col2_min, col2_max = get_map_filter(clean_df, "Enter name of column 2 (int/float) to filter out data for individual plot points only: ")

# create view on dataframe according to inputted filters
mask1 = (clean_df[col1] >= col1_min) & (clean_df[col1] <= col1_max) & (clean_df[col2] >= col2_min) & (clean_df[col2] <= col2_max)
mask2 = (clean_df[col1] >= col1_min) & (clean_df[col1] <= col1_max)
include = clean_df[mask1]

# updated mask for heatmap
mask2 = clean_df[mask2]


map = Map(location=[0, 0], zoom_start=2, control_scale=True)


# plot points using mask1
for index, row in include.iterrows():
    icon = features.CustomIcon("https://i.imgur.com/YCwSiQa.png", icon_size=(53.75,66.25)) # custom icon
    col_names = [col_name for col_name in clean_df.columns.values.tolist()]
    info_wall = ""
    for i, name in enumerate(col_names):
        info_wall = info_wall + name + " " + str(row[name]) + "\n"
    Marker([row["Latitude"], row["Longitude"]],
    popup = info_wall, 
    icon=icon ).add_to(map)

# plot heatmap using mask2
mask2 = mask2[['Latitude', 'Longitude']]
map_data = [[row['Latitude'],row['Longitude']] for index, row in mask2.iterrows()]
HeatMap(map_data).add_to(map)

# save map as html file and open in browser
map.save("./output/map.html")
webbrowser.open('file://' + os.path.realpath("./output/map.html")) # open file in default browser
