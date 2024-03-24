from src.data_ingestion.download_stations import download_stations_data
from src.data_ingestion.download_precipitations import download_precip_data


def main():
    download_stations_data()
    download_precip_data()


if __name__ == "__main__":
    main()
