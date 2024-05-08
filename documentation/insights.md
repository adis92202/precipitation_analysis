# Analysis results & insights

## Preprocessing
- We don't need all the columns which we took from imgw data - basically precipitation data and connected to it 'SMDB status' are needed
- Missing values in different columns (based on [link](https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/Opis.txt)):
    - Missing data for SMDB is good (it means that measurement went as normal), however there are two special codes: 9 means that the meteorogical phenomena did not happen (therefore value 0.0 in column with measurements should be treated as right) and 8 means that the measurement was incorrect - therefore its' values should be treated as NaNs (Not a Numbers)
    - Missing data for Precip type means that the station does not collect information about the type of precipitation. It is not of utmost importance to us, so this data doesn't need to be dropped
    - Missing values for precipitation (in case of Lubusz voivodeship it's one month for one station) can be filled with mean monthly data for whole voivodeship - we can use this simple solution as amplitude of monthly and voivodeship data does not vary much
- Duplicates - by default pandas method `drop_duplicates()`checks if values in all columns match to determine duplicate. For us only station_code and date are enough, as this data should contain daily values and double measurements shouldn't be taken into account. The default behaviour of this function is to leave the first occurance of a duplicate - we could change it to not leaving any duplicates at all (as we cannot be sure which one is true), but we've decided that the default behaviour is good enough. In case of Lubusz voivodeship there are no duplicates.

## Feature engineering
Data types - the data doesn't need many modifications (e.g. the columns do not need scaling) but few of them can be quite useful:
- Combining columns Day Month and Year to obtain a datetime type column with a complete date.
- Changing the types of altitude and snow_cover_cm from integers fo floats.

## EDA
Main conclusions for Lubusz voivodeship:
- The biggest correlations are observed for altitude-lon, altitude-lat, lon-lat which is not delivering any further insights - it is only location data. Columns that are describing precipitation are not significantly correlated to any other features.
- Relationships between particular features are not linear, scatterplots on pairplot show similar information as correlation heatmap.
- Most of the precipitation data describes rain (water), snow is not as important in the analysis.
- Data distributions for precipitation in mm and snow cover in cm are right-skewed - most of the values are close to 0. 
- Most of the higher values of precipitation as treated as outliers - median is close to 0, as mentioned before.
- Data grouped by 6 rivers located in Lubusz voivodeship does not show any particular patterns - distribution look quite similar for each one.
- Similar situation for 7 available stations - all boxplots look very alike.

## SPI analysis
The SPI analysis based on Lubusz voivodeship and its stations is available  in the `SPI_analysis_in_Lubusz.md` file.
Most important conclusions:
- The Lubusz voivodeship has moderate precipitation conditions with a tendency to become drier
- There are periods where it was very rainy
- Rainfall is always moderate in this region
- Lubusz is becoming rainier in the recent years
