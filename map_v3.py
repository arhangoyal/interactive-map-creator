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


def clean_dataset(df):
    clean_df = df.dropna(axis=0)
    clean_df.to_csv("./data/clean_data.csv")

# main
df = pd.read_csv(input("Enter full path to (CSV) dataset on system: "), delimiter=",")

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