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


def find_coordinate_cols(csv_infile):
    # Identify latitude and longitude columns (Assume latitude will be before longitude)
    df = pd.read_csv(csv_infile, delimiter=",")
    # meteorites = meteorites1.dropna(axis=0, inplace=False)
    num_row, num_col = df.shape[0], df.shape[1]
    lat_idx, lon_idx = -1, -1
    coord_col = []

    for col_idx in range(num_col):
        col = df.iloc[: , col_idx] #create a view on column at index col_idx

        # Check if most entries in column are likely to be int/float
        int_percent = 0
        num_tests = randint(100, 200)
        for test_num in range(num_tests): #test randomly on 100 to 200 entries in column being integers
            entry = col[randint(100, num_row-100)] #pick any entry between index 100 index num_row-100 to avoid any padding in data
            if isinstance(entry, int) or isinstance(entry, float):
                int_percent += 1 #number of int/float entries
        int_percent = int_percent * 100 / num_tests # convert to percentage: percent of tests which were int/float

        if int_percent > 90:
            # Check for latitude column
            lat_filter = col[(col >= -90) & (col <= 90)]
            # If more than 80% values are in our coordinates range
            if lat_filter.shape[0] * 100/num_row > 80:
                lat_idx = col_idx
            
            # Check for longitude column
            lon_filter = col[(col >= -180) & (col <= 180)]
            # If more than 80% values are in our coordinates range
            if lon_filter.shape[0] * 100/num_row > 80:
                lon_idx = col_idx

    # Rename the coordinate columns to "Latitude" and "Longitude"
    df.rename(columns={ df.columns[lat_idx]: "Latitude", df.columns[lon_idx]: "Longitude" }, inplace = True)
    # df.rename(columns={ df.columns[coord_col[0]]: "Latitude", df.columns[coord_col[1]]: "Longitude" }, inplace = True)

    # Push the data to outfile
    df.to_csv("./data/coordinate-data-found.csv", index=False)


def clean_coord_data(csv_infile):
    df = pd.read_csv(csv_infile, delimiter=",")
    filtered_coords = (df["Longitude"] >= -180) & (df["Longitude"] <= 180) & (df["Latitude"] >= -90) & (df["Latitude"] <= 90)
    filtered_meteorites = df[filtered_coords]
    df.to_csv("./data/coord-filtered-data.csv", index=False)



# main

infile = input("Enter full/relative path to (CSV) dataset on system: ") # "./data/meteorite-landings.csv"
find_coordinate_cols(infile)
clean_coord_data("./data/coordinate-data-found.csv")