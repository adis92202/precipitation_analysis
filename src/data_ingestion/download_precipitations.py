import pandas as pd
from zipfile import BadZipFile
from .download_changes import download_changes_data
from src.utils.utils import save_df


def get_colnames() -> list[str]:
    """
    Function for getting column names for dataframe

        Returns:
            columns (list[str]): List of column names
    """
    columns = [
        "station_code",
        "station_name",
        "year",
        "month",
        "day",
        "24h_precipitation_mm",
        "SMDB_status",
        "precip_type",
        "snow_cover_cm",
        "PKSN_status",
        "fresh_snow_cover_cm",
        "HSS_status",
        "snow_type_code",
        "GATS_status",
        "snow_cover_type_code",
        "RPSN_status",
    ]

    return columns


def get_urls() -> list[str]:
    """
    Function for creating urls of files to be downloaded

        Returns:
            urls (list[str]): List of all url addresses of files to be downloaded
    """
    base_url = "https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/"
    parent_dirs = ["1991_1995/", "1996_2000/"] + [
        str(i) + "/" for i in range(2001, 2023)
    ]
    child_dirs = [
        [str(i) for i in range(1991, 1996)],
        [str(i) for i in range(1996, 2001)],
    ] + [
        [str(i) + "_" + str(j).zfill(2) for j in range(1, 13)]
        for i in range(2001, 2023)
    ]
    ending = "_o.zip"

    urls = []

    for i in range(len(parent_dirs)):
        p = parent_dirs[i]
        cds = child_dirs[i]
        for cd in cds:
            url = base_url + p + cd + ending
            urls.append(url)

    return urls


def implement_changes(
    precipitation: pd.DataFrame, changes: dict, col: str
) -> pd.DataFrame:
    """Function for implementing changes from 'Opis.txt' file

    Args:
        precipitation (pd.DataFrame): data
        changes (dict): dictionary with changes
        col (str): name of column to implement changes on

    Returns:
        precipitation (pd.DataFrame): DataFrame with implemented changes
    """
    precipitation[col] = precipitation[col].map(changes).fillna(precipitation[col])

    return precipitation


def download_precip_data() -> pd.DataFrame:
    """Function for downloading precipitation data

    Returns:
        precipitation_data_wc (pd.DataFrame): Downloaded precipitation data from 33 years
    """
    print("Beginning downloading precipitation data")
    columns = get_colnames()

    urls = get_urls()

    dfs = []

    for url in urls:
        try:
            precip = pd.read_csv(
                url,
                header=None,
                names=columns,
                encoding="cp1250",
                compression={"method": "zip"},
            )
        except BadZipFile:
            print(f"{url} is corrupted, going to the next file")
            continue

        dfs.append(precip)

    precipitation_data = pd.concat(dfs)

    map_dict = download_changes_data()

    precipitation_data_wc = implement_changes(
        precipitation_data, map_dict, "station_name"
    )

    save_df(
        precipitation_data_wc,
        "precipitation_data.csv",
        "Precipitation data downloaded & saved in data/ directory under 'precipitation_data.csv' name",
    )

    return precipitation_data_wc
