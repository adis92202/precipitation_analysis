import argparse
from src.data_ingestion.download_stations import download_stations_data
from src.data_ingestion.download_precipitations import download_precip_data
from src.visualizations.visualize_stations import visualize, get_voivodeship_names
from src.visualizations.visualize_timeseries_data import visualize_available_data
import os
import geopandas as gpd
import pandas as pd


def main(voi):
    if not os.path.exists("data/stations.shp"):
        download_stations_data()
    elif not os.path.exists("data/precipitation_data.csv"):
        download_precip_data()
    else:
        print(
            "The files precipitation_data.csv and stations.shp already exist in data/ directory."
        )

    precip = pd.read_csv("data/precipitation_data.csv", index_col=0)
    gdf = gpd.read_file("data/stations.shp", encoding="cp1250")
    visualize(gdf, voi)
    visualize_available_data(precip, gdf, voi)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze precipitation data for a specified voivodeship."
    )
    parser.add_argument(
        "--voivodeship",
        type=str,
        default="Lubusz",
        help="The name of the voivodeship (default: Lubusz)",
    )
    args = parser.parse_args()

    voivodeship = args.voivodeship
    available_voivodeships = get_voivodeship_names()
    if voivodeship not in available_voivodeships:
        print(
            "Wrong voivodeship. You can choose among:",
            ", ".join(available_voivodeships),
        )
    else:
        main(voivodeship)
