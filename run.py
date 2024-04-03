import argparse
from src.data_ingestion.download_stations import download_stations_data
from src.data_ingestion.download_precipitations import download_precip_data
from src.visualizations.visualize_stations import visualize
from src.visualizations.visualize_stations import get_voivodeship_names
import os
import geopandas as gpd

def main(voi):
    if not os.path.exists('data/stations.shp'):
        download_stations_data()
    elif not os.path.exists('data/precipitation_data.csv'):  
        download_precip_data()
    else:
        print("The files precipitation_data.csv and stations.shp already exist in data/ directory.")
        gdf = gpd.read_file('data/stations.shp', encoding='cp1250')
        visualize(gdf, voi)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze precipitation data for a specified voivodeship.')
    parser.add_argument('--voivodeship', type=str, default='Lubusz', help='The name of the voivodeship (default: Lubusz)')
    args = parser.parse_args()

    voivodeship = args.voivodeship
    available_voivodeships = get_voivodeship_names()
    if voivodeship not in available_voivodeships:
        print("Wrong voivodeship. You can choose among:", ", ".join(available_voivodeships))
    else:
        main(voivodeship)
