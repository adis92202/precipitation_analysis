import geopandas as gpd
import matplotlib.pyplot as plt
from typing import Tuple

def get_voivodeship_names() -> list:
    """Function to fetch and return a list of voivodeship names with spaces and dashes removed.

    Returns:
        list: A list containing unique names of voivodeships.
    """
    geojson = gpd.read_file('https://simplemaps.com/static/svg/country/pl/admin1/pl.json')
    geojson['name'] = geojson['name'].apply(lambda x: x.replace(' ', '')).apply(lambda x: x.replace('-', ''))
    voivodeships = geojson['name'].unique().tolist()
    return voivodeships

def get_voivodeship_borders() -> gpd.GeoDataFrame:
    """Function to fetch and return voivodeship borders data as GeoDataFrame from a specified URL with spaces and dashes removed from voivodeship names.
    
    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing voivodeship borders
    """
    geojson = gpd.read_file('https://simplemaps.com/static/svg/country/pl/admin1/pl.json')
    geojson['name'] = geojson['name'].apply(lambda x: x.replace(' ', '')).apply(lambda x: x.replace('-', ''))
    return geojson

def clip_to_voivodeship(gdf: gpd.GeoDataFrame, geojson: gpd.GeoDataFrame, voi: str) -> Tuple[gpd.GeoSeries, gpd.GeoDataFrame]:
    """Function to clip GeoDataFrame to specific voivodeship borders
    
    Parameters:
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
    
    Parameters:
        voi_polygon (gpd.GeoSeries): Polygon representing voivodeship borders
        voi_gdf (gpd.GeoDataFrame): GeoDataFrame containing stations data within the voivodeship
        voi (str): Name of the voivodeship

    Returns:
            None
    """

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres')) 
    ax = world.plot(figsize=(10, 10), color='lightgrey')

    voi_polygon.plot(ax=ax, color='none', edgecolor='blue', label=voi) 
    voi_gdf.plot(ax=ax, color='red', markersize=25) 

    for x, y, label in zip(voi_gdf.geometry.x, voi_gdf.geometry.y, voi_gdf['name']):
        ax.text(x, y, label, fontsize=7, ha='left') 

    ax.set_xlim([min(voi_gdf.geometry.x) - 0.75, max(voi_gdf.geometry.x) + 0.75])
    ax.set_ylim([min(voi_gdf.geometry.y) - 0.75, max(voi_gdf.geometry.y) + 0.75])

    plt.title(f'Stations, Voivodeship - {voi}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

def visualize(gdf: gpd.GeoDataFrame, voi: str) -> None:
    """Function to execute the visualization pipeline
    
    Parameters:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing stations data
        voi (str): Name of the voivodeship

    Returns:
            None
    """
    geojson = get_voivodeship_borders()
    voi_polygon, voi_gdf = clip_to_voivodeship(gdf, geojson, voi)
    visualize_stations(voi_polygon, voi_gdf, voi)
