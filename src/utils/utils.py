import pandas as pd
import geopandas as gpd


def save_df(df: pd.DataFrame, name: str, directory: str, message=None) -> None:
    """
    Function for saving DataFrame to .csv file in the given directory with given name

        Args:
            df (pd.DataFrame): DataFrame to be saved
            name (str): Name of file
            directory (str): Name of the directory where the file is being saved
            message (str): Message to be printed

        Returns:
            None
    """
    df.to_csv(directory + "/" + name, encoding="utf-8")
    if message is None:
        print(f"{name} saved in {directory}/")
    else:
        print(message)


def dms_to_dd(coord: str) -> float:
    """
    Function to convert dms to dd

        Args:
            coord (str): Coordinates in dms (degrees minutes seconds) format

        Returns:
            dd (float): Coordinates in dd format
    """
    degrees, minutes, seconds = coord.split()
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    return dd


def save_gdf(gdf: gpd.GeoDataFrame, name: str, iname: str, directory: str, message=None) -> None:
    """
    Function for saving GeoDataFrame to .shp file in given directory with given name and index

        Args:
            gdf (gpd.GeoDataFrame): GeoDataFrame to be saved
            name (str): Name of file
            iname (str): Column name of index
            directory (str): Name of the directory where the file is being saved
            message (str): Message to be printed

        Returns:
            None
    """
    gdf.to_file(directory + "/" + name, index=iname, encoding="cp1250")

    if message is None:
        print(f"Saved gdf to location {directory}/{name}")
    else:
        print(message)


def map_column_names(columns: list) -> list:
    """
    Function to map original column names to more explainable and transparent ones.

    Args:
    columns (list): List of original column names.

    Returns:
    list: List of mapped column names.
    """
    column_mapping = {
        '24h_precipitation_mm': 'Precipitation (mm)',
        'snow_cover_cm': 'Snow Cover (cm)',
    }
    
    return [column_mapping.get(col, col) for col in columns]

