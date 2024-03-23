import pandas as pd
import numpy as np


def download_changes_file() -> pd.DataFrame:
    """Function for downloading file conatining possible stations' name and location changes

    Returns:
        pd.DataFrame: Pandas DataFrame with rows containing description of changes
    """
    changes = pd.read_table(
        "https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/Opis.txt",
        skiprows=72,
        header=None,
        skipinitialspace=True,
        names=["Zmiany"],
    )

    return changes


def split_officials(changes: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Divides changes to the real ones occuring in the precipitation data (not_ofc)
      and to official naming convention (ofc)

    Args:
        changes (pd.DataFrame): DataFrame with rows containing description of changes

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Tuple with real names changes and the official naming convention
    """
    # Dataframe division to changes and official names (these one MAY be unuseful)
    ix = changes[changes["Zmiany"].str.contains("Oficjalna")].index[0]

    changes_not_ofc = changes.iloc[:ix]
    changes_ofc = changes.iloc[ix:]

    return changes_not_ofc, changes_ofc


def create_station_dict(station_names: np.ndarray) -> dict:
    """Funtion creating dictionary with station names mappings

    Args:
        station_names (np.ndarray): Name changes desctiption

    Returns:
        dict: Dictionary to use for mapping purposes
    """
    station_dict = dict()
    for station_name in station_names:
        words = station_name.split()
        # Searching for first occurance of "Stacja"
        first_station_index = words.index("Stacja")
        # Second occurance of "stacja"
        second_station_index = words.index("stacja", first_station_index + 1)
        # Filling dictionary
        station_dict[words[second_station_index + 1].rstrip(",")] = words[
            first_station_index + 1
        ].rstrip(",")
    return station_dict


def download_changes_data() -> dict:
    """Function to execute full changes pipeline

    Returns:
        dict: Dictionary to use for mapping purposes
    """
    changes_df = download_changes_file()
    changes_not_ofc, changes_ofc = split_officials(changes_df)
    changes_not_ofc_dict = create_station_dict(changes_not_ofc["Zmiany"].values)

    return changes_not_ofc_dict
