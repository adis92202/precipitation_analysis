import pandas as pd
import geopandas as gpd


def save_df(df: pd.DataFrame, name: str, message=None) -> None:
    """
    Function for saving DataFrame to .csv file in data/ directory with given name

        Args:
            df (pd.DataFrame): DataFrame to be saved
            name (str): Name of file
            message (str): Message to be printed

        Returns:
            None
    """
    df.to_csv("data/" + name, encoding="utf-8")
    if message is None:
        print(f"{name} saved in data/")
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


def save_gdf(gdf: gpd.GeoDataFrame, name: str, iname: str, message=None) -> None:
    """
    Function for saving GeoDataFrame to .shp file in data/ directory with given name and index

        Args:
            gdf (gpd.GeoDataFrame): GeoDataFrame to be saved
            name (str): Name of file
            iname (str): Column name of index
            message (str): Message to be printed

        Returns:
            None
    """
    gdf.to_file("data/" + name, index=iname, encoding="cp1250")

    if message is None:
        print(f"Saved gdf to location data/{name}")
    else:
        print(message)
