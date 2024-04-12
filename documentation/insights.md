# Analysis results & insights

## Preprocessing
- We don't need all the columns which we took from imgw data - basically precipitation data and connected to it 'SMDB status' are needed
- Missing values in different columns (based on [link](https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/Opis.txt)):
    - Missing data for SMDB is good (it means that measurement went as normal), however there are two special codes: 9 means that the meteorogical phenomena did not happen (therefore value 0.0 in column with measurements should be treated as right) and 8 means that the measurement was incorrect - therefore its' values should be treated as NaNs (Not a Numbers)
    - Missing data for Precip type means that the station does not collect information about the type of precipitation. It is not of utmost importance to us, so this data doesn't need to be dropped
    - Missing values for precipitation (in case of Lubusz voivodeship it's one month for one station) can be filled with mean monthly data for whole voivodeship - we can use this simple solution as amplitude of monthly and voivodeship data does not vary much
- Duplicates - by default pandas method `drop_duplicates()`checks if values in all columns match to determine duplicate. For us only station_code and date are enough, as this data should contain daily values and double measurements shouldn't be taken into account. The default behaviour of this function is to leave the first occurance of a duplicate - we could change it to not leaving any duplicates at all (as we cannot be sure which one is true), but we've decided that the default behaviour is good enough. In case of Lubusz voivodeship there are no duplicates.
- Data types - the data doesn't need many modifications (e.g. the columns do not need scaling) but few of them can be quite useful:
    - Combining columns Day Month and Year to obtain a datetime type column with a complete date.
    - Changing the types of altitude and snow_cover_cm from integers fo floats.



