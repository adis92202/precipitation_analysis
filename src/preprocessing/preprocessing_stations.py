import pandas as pd
import geopandas as gpd
from src.utils.utils import save_df


def get_and_save_missing_stations(
    precip: pd.DataFrame, stations_gdf: gpd.GeoDataFrame
) -> None:
    """Function to find and create list of missing stations - the ones that are available in
       the precipitation data and are not in the stations data. The list is saved to the appropriate file.

    Args:
        precip (pd.DataFrame): Data containing precipitation over years
        stations_gdf (gpd.GeoDataFrame): GeoDataFrame containing details about stations
    """
    merged_df_with_missing = precip.merge(
        stations_gdf, how="left", left_on="station_code", right_on="ID"
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
    save_df(missing_stations_unique, "missing_stations.csv", "data")
