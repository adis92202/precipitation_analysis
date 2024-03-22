import pandas as pd


def download_changes_file():
    changes = pd.read_table(
        "https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/Opis.txt",
        skiprows=72,
        header=None,
        skipinitialspace=True,
        names=["Zmiany"],
    )

    return changes


def split_officials(changes):
    # Dataframe division to changes and official names (these one MAY be unuseful)
    ix = changes[changes["Zmiany"].str.contains("Oficjalna")].index[0]

    changes_not_ofc = changes.iloc[:ix]
    changes_ofc = changes.iloc[ix:]

    return changes_not_ofc, changes_ofc


def create_station_dict(station_names):
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


def download_changes_data():
    changes_df = download_changes_file()
    changes_not_ofc, changes_ofc = split_officials(changes_df)
    changes_not_ofc_dict = create_station_dict(changes_not_ofc["Zmiany"].values)

    return changes_not_ofc_dict
