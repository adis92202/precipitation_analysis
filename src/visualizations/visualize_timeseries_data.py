import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from .visualize_stations import get_voivodeship_borders, clip_to_voivodeship


def clip_precip_to_voi(
    precip: pd.DataFrame, stations_gdf: gpd.GeoDataFrame, voi: str
) -> gpd.GeoDataFrame:
    """Function to clip precipitation data to an only one voivodeship

    Args:
        precip (pd.DataFrame): Data containing precipitation over years
        stations_gdf (gpd.GeoDataFrame): GeoDataFrame containing details about stations
        voi (str): Voivodeship name

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing precipitation data merged with stations' detail from one voivodeship
    """
    vois = get_voivodeship_borders()
    _, voi_gdf = clip_to_voivodeship(stations_gdf, vois, voi)
    return precip.merge(voi_gdf, how="inner", left_on="station_code", right_on="ID")


def prepare_visualization_dataset(merged_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """Function counting number of available months per station per each year

    Args:
        merged_gdf (gpd.GeoDataFrame): GeoDataFrame containing precipitation data merged with stations' detail from one voivodeship

    Returns:
        pd.DataFrame: Pandas DataFrame with columns containing: years, station name and number of available months (0-12)
    """
    pivot_table = merged_gdf.pivot_table(
        index="year", columns="station_name", aggfunc="count"
    )["24h_precipitation_mm"].fillna(0)

    pivot_table_normalized = pivot_table.map(
        lambda x: int(min(x / 12, 12))
    ).reset_index()

    return pivot_table_normalized.melt(id_vars=["year"], value_name="no_months")


def visualize_available_data(
    precip: pd.DataFrame, stations_gdf: gpd.GeoDataFrame, voi: str
) -> None:
    """Visualization of data availability over time for the chosen voivodeship

    Args:
        precip (pd.DataFrame): Data containing precipitation over years
        stations_gdf (gpd.GeoDataFrame): GeoDataFrame containing details about stations
        voi (str): Voivodeship name
    """
    merged_gdf = clip_precip_to_voi(precip, stations_gdf, voi)
    data_to_visualize = prepare_visualization_dataset(merged_gdf)
    sns.set_style("darkgrid")

    fig, ax = plt.subplots(1, 1, figsize=(15, 8))

    sns.scatterplot(
        data_to_visualize,
        x="year",
        y="station_name",
        hue="no_months",
        ax=ax,
        palette="Blues",
    )
    ax.set(
        title=f"Data time range for stations in {voi} voivodeship",
        xlabel="Year",
        ylabel="Station name",
    )
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=7)
    ax.legend(
        loc="center right",
        bbox_to_anchor=(1.1, 0.5),
        title="Number of\nmonths\navailable",
        alignment="center",
    )

    plt.savefig(f"results/{voi}_data_availability.png")
    plt.show()
