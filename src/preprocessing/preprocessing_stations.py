import pandas as pd
import geopandas as gpd
from .clipping import get_voivodeship_borders, clip_to_voivodeship
from src.utils.utils import save_df


def get_and_save_voi_missing_stations(
    precip: pd.DataFrame, stations_gdf: gpd.GeoDataFrame, voi: str
) -> None:
    """Function to find and create list of missing stations in the chosen voivodeship.
       The list is saved to the appropriate file.

    Args:
        precip (pd.DataFrame): Data containing precipitation over years
        stations_gdf (gpd.GeoDataFrame): GeoDataFrame containing details about stations
        voi (str): Voivodeship name
    """
    vois = get_voivodeship_borders()
    _, voi_gdf = clip_to_voivodeship(stations_gdf, vois, voi)
    merged_df_with_missing = precip.merge(
        voi_gdf, how="left", left_on="station_code", right_on="ID"
    )
    merged_df_with_missing = merged_df_with_missing[
        [
            "station_code",
            "station_name",
            "year",
            "month",
            "day",
            "24h_precipitation_mm",
            "precip_type",
            "snow_cover_cm",
            "ID",
            "river",
            "lat",
            "lon",
            "altitude",
        ]
    ]
    missing_stations = merged_df_with_missing[merged_df_with_missing["ID"].isnull()]
    missing_stations_unique = (
        missing_stations[["station_name", "station_code"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    save_df(missing_stations_unique, f"{voi}_missing_stations.csv", "data")
