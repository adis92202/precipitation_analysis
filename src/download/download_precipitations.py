import pandas as pd
from zipfile import BadZipFile
from .download_changes import download_changes_data


def save_df(df, name):
    df.to_csv("../data/" + name)


def get_colnames():
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


def get_urls():
    base_url = "https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/"
    parent_dirs = ["1991_1995/", "1996_2000/"] + [
        str(i) + "/" for i in range(2001, 2024)
    ]
    child_dirs = [
        [str(i) for i in range(1991, 1996)],
        [str(i) for i in range(1996, 2001)],
    ] + [
        [str(i) + "_" + str(j).zfill(2) for j in range(1, 13)]
        for i in range(2001, 2024)
    ]
    ending = "_o.zip"

    return base_url, parent_dirs, child_dirs, ending


def implement_changes(precipitation, changes, col):
    precipitation[col] = precipitation[col].map(changes).fillna(precipitation[col])

    return precipitation


def download_precip_data():
    columns = get_colnames()

    base_url, parent_dirs, child_dirs, ending = get_urls()

    dfs = []

    for i in range(len(parent_dirs)):
        p = parent_dirs[i]
        cds = child_dirs[i]
        for cd in cds:
            url = base_url + p + cd + ending

            try:
                precip = pd.read_csv(
                    url,
                    header=None,
                    names=columns,
                    encoding="cp1250",
                    compression={"method": "zip"},
                )
            except BadZipFile:
                print(f"{cd} is corrupted, going to the next file")
                continue

            dfs.append(precip)

    precipitation_data = pd.concat(dfs)

    map_dict = download_changes_data()

    precipitation_data_wc = implement_changes(
        precipitation_data, map_dict, "station_name"
    )

    save_df(precipitation_data_wc, "precipitation_data.csv")

    return precipitation_data_wc
