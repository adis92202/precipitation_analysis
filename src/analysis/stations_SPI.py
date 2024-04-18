import pandas as pd
import geopandas as gpd
from src.utils.utils import save_df
from src.calculations.calculate_SPI import get_SPI
from src.visualizations.visualize_stations_SPI import (
    visualize_stations_SPI,
    compare_stations_SPI,
    voi_SPI_map,
)


def get_stations_SPI_statistics(
    SPI_1: pd.DataFrame,
    SPI_3: pd.DataFrame,
    SPI_12: pd.DataFrame,
    station_name: str,
    voi: str,
) -> None:
    """Function to generate basic SPI descriptive statistics for a particular station_name in the voi voivodeship.
       The statistics are saved to .csv files.

    Args:
        SPI_1 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one month for a particular station_name.
        SPI_3 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one quater for a particular station_name.
        SPI_12 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one year for a particular station_name.
        station_name (str): Name of the measuring station.
        voi (str): Name of the voivodeship.
    """

    save_df(
        pd.concat(
            [
                SPI_1.describe().rename(columns={"SPI": "Values"}),
                SPI_3.describe().rename(columns={"SPI": "Values"}),
                SPI_12.describe().rename(columns={"SPI": "Values"}),
            ],
            axis=1,
            keys=["SPI_1", "SPI_3", "SPI_12"],
        ),
        f"{station_name}-{voi}_SPI_statistics.csv",
        "results",
    )

    print(
        f"Saved SPIs descriptive statistics from {station_name} station in the {voi} voivodeship in results/{station_name}-{voi}_SPI_statistics.csv"
    )


def stations_SPI_pipeline(
    preprocessed_voi_df: pd.DataFrame, voi_polygon: gpd.GeoDataFrame, voi: str
) -> None:
    """Pipeline for SPI analysis for an each station in the given voivodeship.

    Args:
        preprocessed_voi_df (pd.DataFrame): Pandas DataFrame containing preprocessed data for a given voivodeship.
        voi_polygon (gpd.GeoDataFrame): GeoDataFrame with a polygon containing voivodeship borders.
        voi (str): Voivodeship name.
    """

    station_names = preprocessed_voi_df["station_name"].unique()
    avg_SPIs = pd.DataFrame(
        index=station_names, columns=["SPI_1", "SPI_3", "SPI_12", "lat", "lon"]
    )

    for s in station_names:
        SPI_1, SPI_3, SPI_12 = get_SPI(
            preprocessed_voi_df[preprocessed_voi_df["station_name"] == s],
            voi,
            False,
        )

        avg_SPIs.loc[s, "SPI_1"] = SPI_1["SPI"].mean()
        avg_SPIs.loc[s, "SPI_3"] = SPI_3["SPI"].mean()
        avg_SPIs.loc[s, "SPI_12"] = SPI_12["SPI"].mean()
        avg_SPIs.loc[s, "lat"] = preprocessed_voi_df[
            preprocessed_voi_df["station_name"] == s
        ]["lat"].iloc[0]
        avg_SPIs.loc[s, "lon"] = preprocessed_voi_df[
            preprocessed_voi_df["station_name"] == s
        ]["lon"].iloc[0]

        SPI_1["SPI"] = SPI_1["SPI"].round(2)
        SPI_3["SPI"] = SPI_3["SPI"].round(2)
        SPI_12["SPI"] = SPI_12["SPI"].round(2)

        get_stations_SPI_statistics(SPI_1, SPI_3, SPI_12, s, voi)
        visualize_stations_SPI(SPI_1, SPI_3, SPI_12, s, voi)
        compare_stations_SPI(SPI_1, SPI_3, SPI_12, s, voi)
    voi_SPI_map(avg_SPIs, voi_polygon, voi)
