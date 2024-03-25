import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from typing import Tuple

def get_voivodeship_borders() -> gpd.GeoDataFrame:
    """Function to download and return voivodeship borders data as GeoDataFrame"""
    geojson = gpd.read_file('https://simplemaps.com/static/svg/country/pl/admin1/pl.json')
    return geojson

def clip_to_voivodeship(gdf: gpd.GeoDataFrame, geojson: gpd.GeoDataFrame, voi: str) -> Tuple[gpd.GeoSeries, gpd.GeoDataFrame]:
    """Function to clip GeoDataFrame to specific voivodeship borders
    
    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing stations data
        geojson (gpd.GeoDataFrame): GeoDataFrame containing voivodeship borders
        voi (str): Name of the voivodeship to clip the data to
        
    Returns:
        Tuple[gpd.GeoSeries, gpd.GeoDataFrame]: Tuple containing voivodeship polygon and clipped GeoDataFrame
    """
    voi_polygon = geojson[geojson['name'] == voi]['geometry']
    voi_gdf = gdf[gdf.within(voi_polygon.geometry.iloc[0])]
    return voi_polygon, voi_gdf

def visualize_stations(voi_polygon: gpd.GeoSeries, voi_gdf: gpd.GeoDataFrame, voi: str) -> None:
    """Function to visualize stations within specific voivodeship
    
    Args:
        voi_polygon (gpd.GeoSeries): Polygon representing voivodeship borders
        voi_gdf (gpd.GeoDataFrame): GeoDataFrame containing stations data within the voivodeship
        voi (str): Name of the voivodeship
    """

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres')) 
    ax = world.plot(figsize=(10, 10), color='lightgrey')

    voi_polygon.plot(ax=ax, color='none', edgecolor='blue', label=voi) 
    voi_gdf.plot(ax=ax, color='red', markersize=50) 

    for x, y, label in zip(voi_gdf.geometry.x, voi_gdf.geometry.y, voi_gdf['name']):
        ax.text(x, y, label, fontsize=8, ha='left') 

    ax.set_xlim([min(voi_gdf.geometry.x) - 0.75, max(voi_gdf.geometry.x) + 0.75])
    ax.set_ylim([min(voi_gdf.geometry.y) - 0.75, max(voi_gdf.geometry.y) + 0.75])

    plt.title(f'Stations, Voivodeship - {voi}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

def visualize(gdf: gpd.GeoDataFrame, voi: str) -> None:
    """Function to execute the visualization pipeline
    
    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing stations data
        voi (str): Name of the voivodeship
    """
    geojson = get_voivodeship_borders()
    voi_polygon, voi_gdf = clip_to_voivodeship(gdf, geojson, voi)
    visualize_stations(voi_polygon, voi_gdf, voi)
