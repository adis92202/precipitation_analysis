The code logic, or rather the order of actions taken in this analysis are as follows:

1. Downloading the data for years 1991 - 2022: precipitation, stations, changes in data (as stated by IMGW)
2. Preprocessing:
    1. Clipping the data - clipping all data to voivodeship chosen by the user (default: Lubusz (lubuskie))
    2. Saving missing stations to the file (this currently does not work - you can track an issue [here](https://github.com/adis92202/precipitation_analysis/issues/10))
    3. Cleaning the data - dropping duplicates and setting right NaNs
    4. Filling missing data 
    5. Transforming data types    
3. EDA & Visualizations:
    1. Stations from given voivodeship that are available in the data and are present both in precipitation data & stations data
    2. Available data - plot showing from how many years do we have data for each station
    3. Precipitation data EDA:
        - Basic descriptive statistics, counts and unique counts of values.
        - Time series of precipitation columns (also depending on other features).
        - Distributions of data (histograms, boxplots), relationships between columns (pairplot, correlation - heatmap).
4. SPI Calculations - calculating SPI for three different time windows (1 month, 3 months, 12 months) using gamma distribution.