import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import Point
from src.utils.SPI_utils import map_to_range


def visualize_SPI(
    SPI_1: pd.DataFrame,
    SPI_3: pd.DataFrame,
    SPI_12: pd.DataFrame,
    voi: str,
    station_name: str = None,
) -> None:
    """Visualization of SPIs over time for some particular station_name in some voivodeship (if station_name != None)
       or for a particular voivodeship (if station_name = None).

    Args:
        SPI_1 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one month for a particular station_name.
        SPI_3 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one quater for a particular station_name.
        SPI_12 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one year for a particular station_name.
        voi (str): Name of the voivodeship.
        station_name (str): Name of the measuring station. Defaults to None.
    """

    SPI_1["State"] = SPI_1["SPI"].map(map_to_range)
    SPI_3["State"] = SPI_3["SPI"].map(map_to_range)
    SPI_12["State"] = SPI_12["SPI"].map(map_to_range)
    SPI_dict = {"SPI_1": SPI_1, "SPI_3": SPI_3, "SPI_12": SPI_12}

    color_palette = {
        "Extremely wet": "darkblue",
        "Very wet": "blue",
        "Moderately wet": "cornflowerblue",
        "Moderate conditions": "mediumaquamarine",
        "Moderate drought": "wheat",
        "Severe drought": "sandybrown",
        "Extreme drought": "firebrick",
    }

    hue_order = [
        "Extremely wet",
        "Very wet",
        "Moderately wet",
        "Moderate conditions",
        "Moderate drought",
        "Severe drought",
        "Extreme drought",
    ]

    if station_name:
        plot_title = f"the station {station_name} in {voi} voivodeship"
        plot_suptitle = f"SPIs over time for {station_name} staion in {voi} voivodeship"
        plot_name = f"results/SPIs_{station_name}-{voi}.png"
        message = f"Figure with SPIs for station {station_name} in {voi} voivodeship saved in results/SPIs_{station_name}-{voi}.png"
    else:
        plot_title = f"the {voi} voivodeship"
        plot_suptitle = f"SPIs over time for the {voi} voivodeship"
        plot_name = f"results/SPI_{voi}.png"
        message = f"Figure with SPI over time for the {voi} voivodeship saved in results/SPI_{voi}.png"

    fig, ax = plt.subplots(3, 1, figsize=(14, 17))
    n = 0

    for spi_key, spi_val in SPI_dict.items():

        sns.lineplot(
            spi_val, x=spi_val.index, y="SPI", color="darkgrey", alpha=0.7, ax=ax[n]
        )

        sns.scatterplot(
            spi_val,
            x=spi_val.index,
            y="SPI",
            hue="State",
            ax=ax[n],
            palette=color_palette,
            hue_order=hue_order,
        )

        ax[n].legend(
            title="Precipitation conditions",
            loc="right",
            bbox_to_anchor=(0.69, 0.25, 0.5, 0.5),
        )
        ax[n].set(
            title=f"{spi_key} over time for " + plot_title,
            xlabel="Date",
            ylabel="SPI",
        )
        ax[n].grid(True)
        n += 1

    plt.suptitle(plot_suptitle, y=1, fontsize=16)
    plt.tight_layout()
    plt.savefig(plot_name, bbox_inches="tight")
    plt.close(fig)
    print(message)


def compare_stations_SPI(
    SPI_1: pd.DataFrame, SPI_3: pd.DataFrame, SPI_12: pd.DataFrame, s: str, voi: str
) -> None:
    """Function to compare different SPIs visually for some particular station_name in some voivodeship.

    Args:
        SPI_1 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one month for a particular station_name.
        SPI_3 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one quater for a particular station_name.
        SPI_12 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one year for a particular station_name.
        s (str): Name of the measuring station.
        voi (str): Name of the voivodeship.
    """

    common_index = SPI_1.index.intersection(SPI_3.index).intersection(SPI_12.index)
    SPI_1_common = SPI_1.loc[common_index]
    SPI_3_common = SPI_3.loc[common_index]

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    sns.lineplot(
        SPI_1_common,
        x=SPI_1_common.index,
        y=SPI_1_common["SPI"],
        ax=ax,
        label="SPI_1",
        alpha=0.5,
    )
    sns.lineplot(
        SPI_3_common,
        x=SPI_3_common.index,
        y=SPI_3_common["SPI"],
        ax=ax,
        label="SPI_3",
        alpha=0.5,
    )
    sns.lineplot(
        SPI_12, x=SPI_12.index, y=SPI_12["SPI"], ax=ax, label="SPI_12", alpha=0.5
    )

    ax.set(
        title=f"Comparison of SPIs for station {s} in {voi} voivodeship", xlabel="Year"
    )
    ax.grid(True)
    plt.savefig(f"results/SPI_comparison_{s}-{voi}.png", bbox_inches="tight")
    plt.close(fig)
    print(
        f"Figure with SPIs comparison for station {s} in {voi} voivodeship saved in results/SPI_comparison_{s}-{voi}.png"
    )


def plot_spi_points(
    gdf: gpd.GeoDataFrame,
    ax: plt.axes,
    column: str,
    title: str,
    voi_polygon: gpd.GeoDataFrame,
) -> None:
    """Function to create scatterplot with SPI for a particular ax using column as hue and title as title.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing SPI values with stations locations and its precipitation
                                conditions.
        ax (plt.axes): Matplotlib axis to use while plotting.
        column (str): Column name to use in the scatterplot (SPI_1, SPI_3 or SPI_12).
        title (str): Figure title.
        voi_polygon (gpd.GeoDataFrame): GeoDataFrame with a polygon containing voivodeship borders.
    """

    color_palette = {
        "Extremely wet": "darkblue",
        "Very wet": "blue",
        "Moderately wet": "cornflowerblue",
        "Moderate conditions": "mediumaquamarine",
        "Moderate drought": "wheat",
        "Severe drought": "sandybrown",
        "Extreme drought": "firebrick",
    }

    x, y = voi_polygon.iloc[0].exterior.xy

    ax.plot(x, y, color="blue")
    ax.set_xlim([min(gdf.geometry.x) - 1.25, max(gdf.geometry.x) + 1.25])
    ax.set_ylim([min(gdf.geometry.y) - 0.75, max(gdf.geometry.y) + 0.75])

    sns.scatterplot(
        gdf,
        x=gdf.geometry.x,
        y=gdf.geometry.y,
        hue=column,
        ax=ax,
        palette=color_palette,
    )

    ax.set(title=title, xlabel="Longitude", ylabel="Latitude")
    ax.legend(title="Precipitation conditions")


def voi_SPI_map(
    avg_SPIs: pd.DataFrame, voi_polygon: gpd.GeoDataFrame, voi: str
) -> None:
    """Visualization of average SPIs for a given voivodeship on the map.

    Args:
        avg_SPIs (pd.DataFrame): DataFrame containing average SPIs (SPI_1, SPI_3, SPI_12) with stations locations for a
                                 given voivodeship.
        voi_polygon (gpd.GeoDataFrame): GeoDataFrame with a polygon containing voivodeship borders.
        voi (str): Voivodeship name.
    """

    gdf = gpd.GeoDataFrame(
        avg_SPIs,
        geometry=[
            Point(lon, lat) for lon, lat in zip(avg_SPIs["lon"], avg_SPIs["lat"])
        ],
        crs="EPSG:4326",
    )

    gdf["SPI_1_State"] = gdf["SPI_1"].map(map_to_range)
    gdf["SPI_3_State"] = gdf["SPI_3"].map(map_to_range)
    gdf["SPI_12_State"] = gdf["SPI_12"].map(map_to_range)

    fig, ax = plt.subplots(1, 3, figsize=(30, 10))

    titles = [f"Mean SPI_{i} in {voi} over time" for i in [1, 3, 12]]
    columns = ["SPI_1_State", "SPI_3_State", "SPI_12_State"]

    for i, (column, title) in enumerate(zip(columns, titles)):
        plot_spi_points(gdf, ax[i], column, title, voi_polygon)

    plt.suptitle(f"Mean SPIs over time in the {voi} voivodeship", fontsize=16, y=1)
    plt.tight_layout()
    plt.savefig(f"results/{voi}_SPI_map.png", bbox_inches="tight")
    print(
        f"Figure with map of SPIs in the {voi} voivodeship saved in results/{voi}_SPI_map.png"
    )
