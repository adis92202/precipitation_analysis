import pandas as pd
import numpy as np


def cleaning_data(df: pd.DataFrame, voi: str) -> pd.DataFrame:
    """Function for cleaning data (setting relevant n/a's and dropping duplicates)

    Args:
        df (pd.DataFrame): Precipitation data for given voivodeship
        voi (str): Voivodeship name

    Returns:
        pd.DataFrame: Cleaned data
    """
    print("Cleaning the data...")
    df_smdb = df.copy()
    ind = df_smdb[df_smdb.SMDB_status == 8].index
    df_smdb.loc[ind, "24h_precipitation_mm"] = np.nan

    df_no_duplicates = df_smdb.drop_duplicates(
        subset=["station_code", "year", "month", "day"]
    )

    df_no_duplicates.isna().sum().to_csv(f"data/{voi}_missing_data.csv")

    print(
        f"Cleaning the data ended. File with missing (n/a) data saved to data/{voi}_missing_data.",
        f"{len(df) - len(df_no_duplicates)} duplicates found and dropped",
    )

    return df_no_duplicates


def filling_data(df: pd.DataFrame) -> pd.DataFrame:
    """Function for filling missing values from cleaned data.
    Filled columns are:
        precip_type (with value 'not/available')
        24h_precipitation_mm (with year-monthly mean for the voivodeship)
        SMDB_status (with 'Normal')

    Args:
        df (pd.DataFrame): Cleaned data

    Returns:
        pd.DataFrame: Filled data
    """

    print("Filling missing data...")
    # Precip type
    df_filled = df.copy()
    df_filled["precip_type"] = df_filled.precip_type.fillna("not/available")
    df_filled["precip_type"] = df_filled.precip_type.str.replace("W", "Water").replace(
        "S", "Snow"
    )

    # Precipitation
    years = df_filled.year.unique()
    months = df_filled.month.unique()

    for year in years:
        for month in months:
            temp = df_filled[(df_filled.year == year) & (df_filled.month == month)]
            if temp["24h_precipitation_mm"].isna().sum() > 0:
                ind = temp[temp["24h_precipitation_mm"].isna()].index
                df_filled.loc[ind, "24h_precipitation_mm"] = temp[
                    "24h_precipitation_mm"
                ].mean()

    # SMDB
    df_filled["SMDB_status"] = df_filled["SMDB_status"].fillna("Normal")

    print("Filling missing data ended")

    return df_filled

def transforming_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function performing data transformation to correct data types and prepare for analysis.
    Transformed columns are:
        year, month, date - merged to a date format column
        snow_cover_cm, altitude - int corrected to float

    Args:
        df (pd.DataFrame): Filled data.

    Returns:
        pd.DataFrame: Transformed data.

    """

    print("Transforming data (correcting data types)...")

    df_t = df.copy()
    df_t['date'] = pd.to_datetime(df_t[['year', 'month', 'day']])
    df_t.drop(['year', 'month', 'day'], axis=1, inplace=True)
    df_t.set_index('date', inplace=True)

    df_t['altitude'] = df_t['altitude'].str.replace(' ', '')
    df_t['altitude'] = df_t['altitude'].astype(float)
    df_t['snow_cover_cm'] = df_t['snow_cover_cm'].astype(float)

    print("Transforming data ended.")

    return df_t



def preprocess_precipitation(df: pd.DataFrame, voi: str) -> pd.DataFrame:
    """This is a pipeline function for invoking all preprocessing for the precipitation data
    (except of clipping the data to voivodeship - this is performed separately and earlier)

    Args:
        df (pd.DataFrame): Precipitation data for one voivodeship
        voi (str): Voivodeship name

    Returns:
        pd.DataFrame: Ready to analysis data
    """
    cleaned_df = cleaning_data(df, voi)
    filled_df = filling_data(cleaned_df)
    transformed_df = transforming_data(filled_df)

    return transformed_df
