import pandas as pd
from scipy import stats
from typing import Tuple
from src.utils.utils import save_df


def calculate_SPI(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to calculate Standardized Precipitation Index (SPI) for the given DataFrame.
    The function fits a gamma distribution to the precipitation data and then transforms the
    cumulative distribution function (CDF) of the gamma distribution to calculate the SPI values.
    The returned DataFrame has the same index as the input DataFrame, with each date associated
    with its corresponding SPI value.

    Args:
    df (pd.DataFrame): DataFrame containing the '24h_precipitation_mm' column with precipitation data.

    Returns:
    pd.DataFrame: DataFrame containing SPI for the given data.
    """
    precip_sum = df["24h_precipitation_mm"]
    precip_sum[precip_sum <= 0] = 1e-15
    params = stats.gamma.fit(precip_sum, floc=0)
    shape, loc, scale = params
    cdf = stats.gamma.cdf(precip_sum, shape, loc, scale)
    SPI = stats.norm.ppf(cdf)
    return pd.DataFrame({"SPI": SPI}, index=df.index)


def get_SPI(
    df: pd.DataFrame, voi: str, save=True
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Function to calculate SPI for different periods (SPI-1, SPI-3, SPI-12) and save them to CSV files.

    Args:
    df (pd.DataFrame): DataFrame containing the '24h_precipitation_mm' column with precipitation data.
    voi (str): Name of the analyzed voivodeship.
    save (bool): Flags whether to save the SPI results.

    Returns:
    tuple: Tuple containing SPI-1, SPI-3, and SPI-12 as DataFrames.
    """

    print("Calculating SPI...")

    df.index = pd.to_datetime(df.index)

    SPI_1Y = df.resample("YE").agg({"24h_precipitation_mm": "sum"}).dropna()
    SPI_1 = calculate_SPI(SPI_1Y)

    SPI_3M = df.resample("QE").agg({"24h_precipitation_mm": "sum"}).dropna()
    SPI_3 = calculate_SPI(SPI_3M)

    SPI_1M = df.resample("ME").agg({"24h_precipitation_mm": "sum"}).dropna()
    SPI_12 = calculate_SPI(SPI_1M)

    if save:
        save_df(SPI_1, f"{voi}_SPI_yearly.csv", "results")
        save_df(SPI_3, f"{voi}_SPI_quarterly.csv", "results")
        save_df(SPI_12, f"{voi}_SPI_monthly.csv", "results")

    print("SPI calculated.")

    return SPI_1, SPI_3, SPI_12
