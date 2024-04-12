import argparse
from src.data_ingestion.download_data import get_data
from src.visualizations.visualize_stations import (
    visualize_stations,
    get_voivodeship_names,
)
from src.visualizations.visualize_timeseries_data import visualize_available_voi_data
from src.preprocessing.preprocessing_stations import get_and_save_voi_missing_stations
from src.preprocessing.clipping import clip_data_to_voi
from src.preprocessing.preprocessing_precip import preprocess_precipitation
from src.calculations.obtain_basic_statistics import get_basic_statistics
from src.utils.utils import save_df
from src.visualizations.visualize_EDA_results import visualize_EDA
from src.calculations.calculate_SPI import get_SPI
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


def main(voi):
    # Data acquisition
    all_precip, stations = get_data()

    # Preprocessing
    voi_polygon, voi_precip, voi_stations = clip_data_to_voi(all_precip, stations, voi)
    get_and_save_voi_missing_stations(all_precip, stations, voi)
    preprocessed_df = preprocess_precipitation(voi_precip, voi)

    # After ALL preprocessing is done - save the precip file (not earlier!)
    save_df(preprocessed_df, f"preprocessed_{voi}_data.csv")

    # Obtaining basic statistics for preprocessed data
    get_basic_statistics(preprocessed_df)
    
    # Visualizations
    visualize_stations(voi_polygon, voi_stations, voi)
    visualize_available_voi_data(voi_precip, voi)

    # EDA visualizations for precipitation data
    visualize_EDA(preprocessed_df, voi)

    # SPI calculations for precipitation data
    SPI_1, SPI_3, SPI_12 = get_SPI(preprocessed_df)


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
