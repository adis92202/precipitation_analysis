import pandas as pd
from src.utils.utils import save_df


def get_basic_statistics(df: pd.DataFrame, voi: str) -> None:
    """
    Function to obtain basic statistics for the DataFrame describing given voivodeship and save them to CSV files.

    This function calculates basic statistics for the input DataFrame, including descriptive statistics,
    counts of non-null values, and counts of unique values for each column. It saves these statistics to
    separate CSV files.

    Args:
        df (pd.DataFrame): Input DataFrame for which basic statistics will be calculated.
        voi (str): Name of the analyzed voivodeship.

    Returns:
        None
    """

    print("Obtaining basic statistics...")
    save_df(df.describe(), f"{voi}_precip_description_table.csv", "results")

    c = df.count()
    c_loc = f"results/{voi}_precip_counts_table.csv"
    c.to_csv(c_loc, header=False)
    print(f"Saved precip data descriptive statistics from {voi} voivodeship in {c_loc}")

    nu = df.nunique()
    nu_loc = f"results/{voi}_precip_unique_values_table.csv"
    nu.to_csv(nu_loc, header=False)
    print(
        f"Saved precip data counts of unique values from {voi} voivodeship in {nu_loc}"
    )

    print("Obtained basic statistics.")
