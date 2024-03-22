import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


def move_right(row):
    rzeka_index = 2
    if str(row["river"])[0].isdigit():
        for i in range(len(row) - 1, rzeka_index, -1):
            row.iloc[i] = row.iloc[i - 1]
        row.iloc[rzeka_index] = None
    return row


def dms_to_dd(coord):
    degrees, minutes, seconds = coord.split()
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    return dd


def get_column_names():
    return ["N", "ID", "name", "river", "lat", "lon", "altitude"]


def create_gdf(df):
    # Creating column with Point geometry
    geometry = [Point(lon, lat) for lon, lat in zip(df["lon"], df["lat"])]

    # Creating GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    return gdf


def save_gdf(gdf, name, iname):
    gdf.to_file("data/" + name, index=iname)


def download_stations_data():
    col_names = get_column_names()

    stations = pd.read_csv(
        "https://danepubliczne.imgw.pl/pl/datastore/getfiledown/Arch/Telemetria/Meteo/kody_stacji.csv",
        sep=";",
        encoding="cp1250",
        index_col=0,
        header=0,
        names=col_names,
    )

    stations = stations.apply(move_right, axis=1)

    stations["lon"] = stations["lon"].apply(dms_to_dd)
    stations["lat"] = stations["lat"].apply(dms_to_dd)

    stations_gdf = create_gdf(stations)

    save_gdf(stations_gdf, "stations.shp", "N")

    return stations_gdf
