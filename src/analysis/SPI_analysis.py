import os
import pandas as pd
import geopandas as gpd
from src.utils.utils import save_df
from src.calculations.calculate_SPI import get_SPI
from src.visualizations.visualize_SPI import (
    visualize_SPI,
    compare_stations_SPI,
    voi_SPI_map,
)


def get_SPI_statistics(
    SPI_1: pd.DataFrame,
    SPI_3: pd.DataFrame,
    SPI_12: pd.DataFrame,
    voi: str,
    station_name: str = None,
) -> None:
    """Function to generate basic SPI descriptive statistics for a particular station_name in the voi voivodeship
       or for the entire voivodeship (depends on station_name argument). The statistics are saved to .csv files.

    Args:
        SPI_1 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one month for a particular station_name.
        SPI_3 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one quater for a particular station_name.
        SPI_12 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one year for a particular station_name.
        voi (str): Name of the voivodeship.
        station_name (str): Name of the measuring station. Defaults to None
    """

    spi_stats_df = pd.concat(
        [
            SPI_1.describe().rename(columns={"SPI": "Values"}),
            SPI_3.describe().rename(columns={"SPI": "Values"}),
            SPI_12.describe().rename(columns={"SPI": "Values"}),
        ],
        axis=1,
        keys=["SPI_1", "SPI_3", "SPI_12"],
    )

    if station_name:
        message = f"Saved SPIs descriptive statistics for {station_name} station in the {voi} voivodeship in results/{station_name}-{voi}_SPI_statistics.csv"
        plot_name = f"{station_name}-{voi}_SPI_statistics.csv"
    else:
        message = f"Saved SPIs descriptive statistics for {voi} voivodeship in results/{voi}_SPI_statistics.csv"
        plot_name = f"{voi}_SPI_statistics.csv"

    save_df(
        spi_stats_df,
        plot_name,
        "results",
        message,
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
        if get_SPI(
            preprocessed_voi_df[preprocessed_voi_df["station_name"] == s],
            voi,
            False,
        ):
            SPI_1, SPI_3, SPI_12 = get_SPI(
                preprocessed_voi_df[preprocessed_voi_df["station_name"] == s],
                voi,
                False,
            )

            SPI_1["SPI"] = SPI_1["SPI"].round(2)
            SPI_3["SPI"] = SPI_3["SPI"].round(2)
            SPI_12["SPI"] = SPI_12["SPI"].round(2)

            get_SPI_statistics(SPI_1, SPI_3, SPI_12, voi, s)
            visualize_SPI(SPI_1, SPI_3, SPI_12, voi, s)
            compare_stations_SPI(SPI_1, SPI_3, SPI_12, s, voi)
        avg_SPIs.loc[s, "SPI_1"] = SPI_1["SPI"].mean()
        avg_SPIs.loc[s, "SPI_3"] = SPI_3["SPI"].mean()
        avg_SPIs.loc[s, "SPI_12"] = SPI_12["SPI"].mean()
        avg_SPIs.loc[s, "lat"] = preprocessed_voi_df[
            preprocessed_voi_df["station_name"] == s
        ]["lat"].iloc[0]
        avg_SPIs.loc[s, "lon"] = preprocessed_voi_df[
            preprocessed_voi_df["station_name"] == s
        ]["lon"].iloc[0]
    voi_SPI_map(avg_SPIs, voi_polygon, voi)


def voi_SPI_pipeline(preprocessed_voi_df: pd.DataFrame, voi: str) -> None:
    """Pipeline for SPI analysis for a given voivodeship.

    Args:
        preprocessed_voi_df (pd.DataFrame): Pandas DataFrame containing preprocessed data for a given voivodeship.
        voi (str): Voivodeship name.
    """
    if (
        (not os.path.exists(f"results/{voi}_SPI_monthly.csv"))
        or (not os.path.exists(f"results/{voi}_SPI_quarterly.csv"))
        or (not os.path.exists(f"results/{voi}_SPI_yearly.csv"))
    ):
        SPI_1, SPI_3, SPI_12 = get_SPI(
            preprocessed_voi_df,
            voi,
            True,
        )
    else:
        SPI_1 = pd.read_csv(
            f"results/{voi}_SPI_yearly.csv", index_col="date", parse_dates=True
        )
        SPI_3 = pd.read_csv(
            f"results/{voi}_SPI_quarterly.csv", index_col="date", parse_dates=True
        )
        SPI_12 = pd.read_csv(
            f"results/{voi}_SPI_monthly.csv", index_col="date", parse_dates=True
        )

    SPI_1["SPI"] = SPI_1["SPI"].round(2)
    SPI_3["SPI"] = SPI_3["SPI"].round(2)
    SPI_12["SPI"] = SPI_12["SPI"].round(2)

    get_SPI_statistics(SPI_1, SPI_3, SPI_12, voi)
    visualize_SPI(SPI_1, SPI_3, SPI_12, voi)
