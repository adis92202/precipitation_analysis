from src.data_ingestion.download_stations import download_stations_data
from src.data_ingestion.download_precipitations import download_precip_data
from src.visualizations.visualize_stations import visualize
import os
import geopandas as gpd

def main():
    if not os.path.exists('data/stations.shp'):
        download_stations_data()
    elif not os.path.exists('data/precipitation_data.csv'):  
        download_precip_data()
    else:
        print("The file precipitation_data.csv and stations.shp already exist in data/ directory.")
        gdf = gpd.read_file('data/stations.shp')
        voi = "Lubusz"
        visualize(gdf,voi)
        
if __name__ == "__main__":
    main()
