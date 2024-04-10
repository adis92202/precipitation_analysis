import os
from .download_stations import download_stations_data
from .download_precipitations import download_precip_data
import pandas as pd
import geopandas as gpd
from typing import Tuple


def get_data() -> Tuple[pd.DataFrame, gpd.GeoDataFrame]:
    """Pipeline for getting data

    Returns:
        Tuple[pd.DataFrame, gpd.GeoDataFrame]: All precipitation data & stations data
    """
    print("Reading the data...")

    if not os.path.exists("data/stations.shp"):
        download_stations_data()
    else:
        print("precipitation_data.csv already exists in data/ directory")

    if not os.path.exists("data/precipitation_data.csv"):
        download_precip_data()
    else:
        print("stations.shp already exists in data/ directory.")

    all_precip = pd.read_csv(
        "data/precipitation_data.csv",
        index_col=0,
        dtype={"snow_cover_type_code": "object"},
    )
    stations_gdf = gpd.read_file("data/stations.shp", encoding="cp1250")

    print("Reading the data ended")
    return all_precip, stations_gdf
