import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


def move_right(row: pd.Series) -> pd.Series:
    """
    In some records columns with lat and lon are shifted, this function solves this problem

        Parameters:
            row (pd.Series): Row to be fixed

        Returns:
            row (pd.Series): Fixed row
    """
    rzeka_index = 2
    if str(row["river"])[0].isdigit():
        for i in range(len(row) - 1, rzeka_index, -1):
            row.iloc[i] = row.iloc[i - 1]
        row.iloc[rzeka_index] = None
    return row


def dms_to_dd(coord: str) -> float:
    """
    Function to convert dms to dd

        Parameters:
            coord (str): Coordinates in dms (degrees minutes seconds) format

        Returns:
            dd (float): Coordinates in dd format
    """
    degrees, minutes, seconds = coord.split()
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    return dd


def get_column_names() -> list[str]:
    """
    Function for getting column names for GeoDataFrame

        Returns:
            columns (list[str]): List of column names
    """

    columns = ["N", "ID", "name", "river", "lat", "lon", "altitude"]
    return columns


def create_gdf(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Function for creating GeoDataFrame from pandas DataFrame

        Parameters:
            df (pd.DataFrame): DataFrame with lat and lon columns

        Returns:
            gdf (gpd.GeoDataFrame): GeoDataFrame with coordinates system EPSG:4326
    """
    geometry = [Point(lon, lat) for lon, lat in zip(df["lon"], df["lat"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    return gdf


def save_gdf(gdf: gpd.GeoDataFrame, name: str, iname: str) -> None:
    """
    Function for saving GeoDataFrame to .shp file in data/ directory with given name and index

        Parameters:
            gdf (gpd.GeoDataFrame): GeoDataFrame to be saved
            name (str): Name of file
            iname (str): Column name of index

        Returns:
            None
    """
    gdf.to_file("data/" + name, index=iname, encoding="cp1250")


def download_stations_data() -> gpd.GeoDataFrame:
    """
    Function for downloading stations data

        Returns:
            stations_gdf (gpd.GeoDataFrame): GeoDataFrame of stations
    """

    print("Beginning downloading stations data")
    col_names = get_column_names()

    stations = pd.read_csv(
        "https://danepubliczne.imgw.pl/pl/datastore/getfiledown/Arch/Telemetria/Meteo/kody_stacji.csv",
        sep=";",
        encoding="cp1250",
        index_col=0,
        header=0,
        names=col_names,
    )

    stations = stations.apply(move_right, axis=1)

    stations["lon"] = stations["lon"].apply(dms_to_dd)
    stations["lat"] = stations["lat"].apply(dms_to_dd)

    stations_gdf = create_gdf(stations)

    save_gdf(stations_gdf, "stations.shp", "N")

    print(
        "Stations data downloaded & saved in data/ directory under 'stations.shp' name"
    )

    return stations_gdf
