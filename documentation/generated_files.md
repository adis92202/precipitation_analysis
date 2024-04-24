## Generated files

This file aims to describe what files are produced during the analysis. 
Files are generated in two directories: 
- in the data/ directory you will find 'raw' data - intermediate or final data that is used during analysis
- in the results/ directory you will find final results such as plots or descriptive statistics

### data/ directory

**precipitation_data.csv** - precipitation data downloaded from IMGW website from years 1991-2022. It's data with correct column names (as mapped in 'column_names.md' file), from all voivodeships with correct station names (if they had changed across the time)

**stations.shp (and other extentions)** - shapefile of all stations in Poland. It consists of station name, station ID, coordinates (latitude and longitude) and river name that is near the station.

**[voivodeship_name]_missing_data.csv** - number of NAs (null values) in data before its' filling .

**preprocessed_[voivodeship_name]_data.csv** - preprocessed data from given voivodeship. It has both precipitation & stations' data. Missing precipitation data is filled with monthly means. 

**missing_stations.csv** - stations that are missing from the analysis across the whole dataset. The reason for not having those stations in analysis is because they are not present in the file shared by IMGW containing stations data.

### results/ directory

#### Data

**[station_name]-[voivodeship_name]_SPI_statistics.csv** - SPI statistics for each and every station from analysed voivodeship. It contains basic descriptive statistics for the station for each SPI type (SPI-1, SPI-3 and SPI-12).

**[voivodeship_name]_precip_counts_table.csv** - Number of records with data for every column - for confirmation purposes.

**[voivodeship_name]_precip_description_table.csv** - Basic descriptive statistics for precipitation data from given voivodeship.

**[voivodeship_name]_precip_unique_values_table.csv** - Number of unique values in each column of precipitation data.

**[voivodeship_name]_SPI_monthly.csv** - Values of SPI-1

**[voivodeship_name]_SPI_quaterly.csv** - Values of SPI-3

**[voivodeship_name]_SPI_yearly.csv** - Values of SPI-12

**[voivodeship_name]_SPI_statistics.csv** - SPI statistics for whole voivodeship. It contains basic descriptive statistics for each SPI type (SPI-1, SPI-3 and SPI-12).

#### Plots

**[voivodeship_name]_data_availability.png** - Plot of data availability for every station in given voivodeship. Color of a dot resembles number of months from which data is available in each year.

**[voivodeship_name]_precip_boxplos.png** - Boxplot of precipitation data.

**[voivodeship_name]_precip_boxplot_precip_type_data.png** - Boxplots of precipitation data with division by precipitation type (snow, rain or not available).

**[voivodeship_name]_precip_boxplot_river_data.png** - Boxplots of precipitation data with division by rivers.

**[voivodeship_name]_precip_boxplot_station_name_data.png** - Boxplots of precipitation data with division by stations.

**[voivodeship_name]_precip_correlations.png** - Matrix of correlations between arguments as a heatmap.

**[voivodeship_name]_precip_histplots.png** - Distribution of precipitation and snow cover values.

**[voivodeship_name]_precip_monthly_time_series.png** - Time series for precipitation and snow cover values in each month.

**[voivodeship_name]_precip_time_series_precip_type_data.png** - Time series for precipitation with division by precipitation type (snow rain or not available).

**[voivodeship_name]_precip_pairplot.png** - Pairplot of the data.

**[voivodeship_name]_SPI_map.png** - Mean different types of SPI values for each station.

**[voivodeship_name]_stations.png** - Stations' localizations for voivodeship.

**SPI_[voivodeship_name].png** - Values of different SPIs across time for whole voivodeship

**SPIs_[station_name]-[voivodeship_name].png** - Values of different SPIs across time for each station

**SPI_comparision_[station_name]-[voivodeship_name].png** - Values of different SPIs across time for each station on the same plot (for comparision purposes)






