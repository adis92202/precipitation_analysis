The code logic, or rather the order of actions taken in this analysis are as follows:

1. Downloading the data for years 1991 - 2022: precipitation, stations, changes in data (as stated by IMGW)
2. Preprocessing:
    1. Clipping the data - clipping all data to voivodeship chosen by the user (default: Lubusz (lubuskie))
    2. Saving missing stations to the file (this currently does not work - you can track an issue [here](https://github.com/adis92202/precipitation_analysis/issues/10))
3. Visualizations:
    1. Stations from given voivodeship that are available in the data and are present both in precipitation data & stations data
    2. Available data - plot showing from how many years do we have data for each station