import pandas as pd
from scipy import stats
from typing import Tuple
from src.utils.utils import save_df

def calculate_SPI(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Function to calculate Standardized Precipitation Index (SPI) for the given DataFrame.

    Args:
    df (pd.DataFrame): DataFrame containing the '24h_precipitation_mm' column with precipitation data.
    window (int): Window size in days to compute the precipitation sum.

    Returns:
    pd.DataFrame: DataFrame containing SPI for the given data.
    """
    precip_sum = df['24h_precipitation_mm'].rolling(window=window).sum().dropna()
    params = stats.gamma.fit(precip_sum, floc=0)
    shape, loc, scale = params
    cdf = stats.gamma.cdf(precip_sum, shape, loc, scale)
    SPI = stats.norm.ppf(cdf)
    return pd.DataFrame(SPI)

def get_SPI(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Function to calculate SPI for different periods (SPI-1, SPI-3, SPI-12) and save them to CSV files.

    Args:
    df (pd.DataFrame): DataFrame containing the '24h_precipitation_mm' column with precipitation data.

    Returns:
    tuple: Tuple containing SPI-1, SPI-3, and SPI-12 as DataFrames.
    """

    print("Calculating SPI...")

    SPI_1 = calculate_SPI(df, window=30)
    SPI_3 = calculate_SPI(df, window=90)
    SPI_12 = calculate_SPI(df, window=365)
    save_df(SPI_1,'SPI_1.csv')
    save_df(SPI_3,'SPI_3.csv')
    save_df(SPI_12,'SPI_12.csv')

    print("Calculated SPI.")

    return SPI_1, SPI_3, SPI_12
