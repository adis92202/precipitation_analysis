import os
import pandas as pd
from src.utils.utils import save_df
from src.calculations.calculate_SPI import get_SPI
from src.visualizations.visualize_voi_SPI import visualize_voi_SPI


def get_voi_SPI_statistics(
    SPI_1: pd.DataFrame, SPI_3: pd.DataFrame, SPI_12: pd.DataFrame, voi: str
) -> None:
    """Function to generate basic SPI descriptive statistics for a particular voivodeship.
       The statistics are saved to .csv files.

    Args:
        SPI_1 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one month for a particular voivodeship.
        SPI_3 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one quater for a particular voivodeship.
        SPI_12 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one year for a particular voivodeship.
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
        f"{voi}_SPI_statistics.csv",
        "results",
    )
    print(
        f"Saved SPIs descriptive statistics from {voi} voivodeship in results/{voi}_SPI_statistics.csv"
    )


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

    get_voi_SPI_statistics(SPI_1, SPI_3, SPI_12, voi)
    visualize_voi_SPI(SPI_1, SPI_3, SPI_12, voi)
