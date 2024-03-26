import argparse
from src.data_ingestion.download_stations import download_stations_data
from src.data_ingestion.download_precipitations import download_precip_data
from src.visualizations.visualize_stations import visualize
import os
import geopandas as gpd

AVAILABLE_VOIVODESHIPS = [
    "Silesian", "Lesser Poland", "Subcarpathian", "Lower Silesian", "Opole",
    "Podlachian", "Warmian-Masurian", "Lubusz", "West Pomeranian", "Lublin",
    "Pomeranian", "Masovian", "Łódź", "Kuyavian-Pomeranian", "Greater Poland",
    "Świętokrzyskie"
]

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
    if voivodeship not in AVAILABLE_VOIVODESHIPS:
        print("Wrong voivodeship. You can choose among:", ", ".join(AVAILABLE_VOIVODESHIPS))
    else:
        main(voivodeship)
