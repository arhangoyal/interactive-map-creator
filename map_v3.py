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


def find_coordinate_cols(csv_infile, csv_outfile):


    # Identify latitude and longitude columns (Assume latitude will be before longitude)
    df = pd.read_csv(csv_infile, delimiter=",")
    # meteorites = meteorites1.dropna(axis=0, inplace=False)
    num_row = df.shape[0]
    num_col = df.shape[1]
    coord_col = []
    for col_idx in range(num_col):
        temp = df.iloc[: , col_idx] #create a view on column at index col_idx

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

    # Rename the coordinate columns to "Latitude" and "Longitude"
    df.rename(columns={ df.columns[coord_col[0]]: "Latitude", df.columns[coord_col[1]]: "Longitude" }, inplace = True)

    # Push the data to outfile
    df.to_csv(csv_outfile)



# main

infile = input("Enter full/relative path to (CSV) dataset on system: ") # "./data/meteorite-landings.csv"
outfile = input("Enter full/relative path to output file on system: ") # "./data/coordinate-data-found.csv"
find_coordinate_cols(infile, outfile)