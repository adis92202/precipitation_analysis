import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from src.utils.utils import dms_to_dd, save_gdf


def move_right(row: pd.Series) -> pd.Series:
    """
    In some records columns with lat and lon are shifted, this function solves this problem

        Args:
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


def get_column_names() -> list[str]:
    """
    Function for getting column names for GeoDataFrame

        Returns:
            columns (list[str]): List of column names
    """

    columns = ["N", "ID", "name", "river", "lat", "lon", "altitude"]
    return columns


def create_stations_gdf(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Function for creating GeoDataFrame from pandas DataFrame

        Args:
            df (pd.DataFrame): DataFrame with lat and lon columns

        Returns:
            gdf (gpd.GeoDataFrame): GeoDataFrame with coordinates system EPSG:4326
    """
    geometry = [Point(lon, lat) for lon, lat in zip(df["lon"], df["lat"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    return gdf


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

    stations_gdf = create_stations_gdf(stations)

    save_gdf(
        stations_gdf,
        "stations.shp",
        "N",
        "data",
        "Stations data downloaded & saved in data/ directory under 'stations.shp' name",
    )

    return stations_gdf
