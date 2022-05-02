# interactive-map-creator
Interactive Map Creator

## Link to Meteorite Dataset

[NASA Meteorite Landings](https://www.kaggle.com/datasets/nasa/meteorite-landings)

## Abstract

Maps are wonderful. They can take a huge CSV file and present it in a condensed form, making it easier for the human brain to process the data. Interactive maps are even better. They allow the viewer to interact with data on a fundamentally new level. Data scientists, meteorologists, historians, and several other professions involve analyzing decades of data. Many of these applications involve studying trendlines or even the concentration of events from a particular time period in various regions of the world. For instance, people studying meteorites may want to analyze heatmaps or individual meteorites from different time periods.

As someone who loves visual and interactive ways of learning and working, I have created a tool to create an interactive heatmap for any inputted dataset with map data (latitude, longitude). To make the interface clean for the user, I designed a solution to identify the latitude and longitude columns in the input dataset and use it to create an interactive heatmap. I then overlay the heatmap with individual datapoints (clickable icons with an information wall) based on a filter which the user creates. The idea is that while we may want to observe the pattern shown by a neat heatmap, we might only want to see information about specific “important” plot points. I feel this is a beautiful way to view the pattern/general trend and important data points together.

Note: The heatmap and icon sizes adjust themselves as users zoom in and out of the map!

## Implementation Details

I have split the program into two files: [interactive-map-creator.py](interactive-map-creator.py) and [myfunctions](myfunctions.py). The former contains the main program, and the latter is a library I have creator to make my main program neater.

Although this program can be used with any input dataset (after commenting out the meteorite data specific clean up in [interactive-map-creator.py](interactive-map-creator.py)), I have used the meteorite data as a base for my project.

1. I have added the input dataset I downloaded: [meteorite-landings](./input/meteorite-landings.csv).
2. The output is a map which is automatically opened on your device's default web browser when the program is run.
3. I have attached my [sample map output](./output/map.html) for data in time (year) span [1960, 2016] and mass (kg) range [100, 100000].
4. I have also added a [sample output picture](./output/sample_output.png) and a [sample output video](./output/honors_project.mp4) to the [same folder](./output/).
5. The [data folder](./data/) contains the intermediate CSV files the program creates in its journey from the input dataset to the output map.

## Future Works

1. I would like to create and use a training set to figure out the ideal latitude and longitude value percentage buffers (currently 80%) to maximize accuracy when dealing with different datasets.
2. I would also like to figure out a way to make the information wall (which appears on clicking map icons) more pleasant to look at.
3. I also had an idea to create a more advanced heatmap which can tell the user the density of datapoints in a particular region around the mouse pointer (say 2% radius of image size in current zoom level).
