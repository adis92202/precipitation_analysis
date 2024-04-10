import pandas as pd
import geopandas as gpd
from typing import Tuple


def clip_precip_to_voi(precip: pd.DataFrame, voi_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """Function to clip precipitation data to only one voivodeship

    Args:
        precip (pd.DataFrame): Data containing precipitation over years
        voi_gdf (gpd.GeoDataFrame): GeoDataFrame containing details about stations from given voivodeship

    Returns:
        pd.DataFrame: DataFrame containing precipitation data merged with stations'
                      detail from one voivodeship
    """

    merged_df = precip.merge(
        voi_gdf, how="inner", left_on="station_code", right_on="ID"
    )
    merged_df = merged_df[
        [
            "station_code",
            "station_name",
            "year",
            "month",
            "day",
            "24h_precipitation_mm",
            "SMDB_status",
            "precip_type",
            "snow_cover_cm",
            "river",
            "lat",
            "lon",
            "altitude",
        ]
    ]

    return merged_df


def clip_to_voivodeship(
    gdf: gpd.GeoDataFrame, geojson: gpd.GeoDataFrame, voi: str
) -> Tuple[gpd.GeoSeries, gpd.GeoDataFrame]:
    """Function to clip GeoDataFrame to specific voivodeship borders

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing stations data
        geojson (gpd.GeoDataFrame): GeoDataFrame containing voivodeship borders
        voi (str): Name of the voivodeship to clip the data to

    Returns:
        Tuple[gpd.GeoSeries, gpd.GeoDataFrame]: Tuple containing voivodeship polygon
                                                and clipped GeoDataFrame
    """
    voi_polygon = geojson[geojson["name"] == voi]["geometry"]
    voi_gdf = gdf[gdf.within(voi_polygon.geometry.iloc[0])]
    return voi_polygon, voi_gdf


def get_voivodeship_borders() -> gpd.GeoDataFrame:
    """Function to fetch and return voivodeship borders data as GeoDataFrame from
       a specified URL with spaces and dashes removed from voivodeship names.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing voivodeship borders
    """
    geojson = gpd.read_file(
        "https://simplemaps.com/static/svg/country/pl/admin1/pl.json"
    )
    geojson["name"] = (
        geojson["name"]
        .apply(lambda x: x.replace(" ", ""))
        .apply(lambda x: x.replace("-", ""))
    )
    return geojson


def clip_data_to_voi(
    precip: pd.DataFrame, stations: gpd.GeoDataFrame, voi: str
) -> list[gpd.GeoDataFrame, gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Pipeline for clipping all the data to voivodeships

    Args:
        precip (pd.DataFrame): All precipitation data
        stations (gpd.GeoDataFrame): All stations data
        voi (str): Voivodeship name

    Returns:
        list[gpd.GeoDataFrame, gpd.GeoDataFrame, gpd.GeoDataFrame]: Polygon of voivodeship, precipitation data clipped
          to voivodeship & stations clipped to voivodeship
    """
    print(f"Clipping pecipitation and stations data to {voi} voivodeship...")
    geojson = get_voivodeship_borders()
    voi_polygon, voi_stations_gdf = clip_to_voivodeship(stations, geojson, voi)
    voi_precip_gdf = clip_precip_to_voi(precip, voi_stations_gdf)

    print("Clipping ended")

    return voi_polygon, voi_precip_gdf, voi_stations_gdf
