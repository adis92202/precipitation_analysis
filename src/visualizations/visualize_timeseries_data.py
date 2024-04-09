import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns


def prepare_visualization_dataset(merged_df: pd.DataFrame) -> pd.DataFrame:
    """Function counting number of available months per station per each year

    Args:
        merged_df (pd.DataFrame): DataFrame containing precipitation data merged
                                  with stations' details from one voivodeship

    Returns:
        pd.DataFrame: Pandas DataFrame with columns containing: years, station
                      name and number of available months (0-12)
    """
    pivot_table = merged_df.pivot_table(
        index="year", columns="station_name", aggfunc="count"
    )["24h_precipitation_mm"].fillna(0)

    pivot_table_normalized = pivot_table.map(
        lambda x: int(min(x / 12, 12))
    ).reset_index()

    return pivot_table_normalized.melt(id_vars=["year"], value_name="no_months")


def visualize_available_voi_data(voi_precip: gpd.GeoDataFrame, voi: str) -> None:
    """Visualization of data availability over time for the chosen voivodeship

    Args:
        voi_precip (gpd.GeoDataFrame): Precip data clipped to the voivodeship
        voi (str): Voivodeship name
    """

    data_to_visualize = prepare_visualization_dataset(voi_precip)
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
    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=7)
    ax.legend(
        loc="center right",
        bbox_to_anchor=(1.1, 0.5),
        title="Number of\nmonths\navailable",
        alignment="center",
    )

    plt.get_current_fig_manager().set_window_title(
        f"Data time range for stations in {voi} voivodeship"
    )
    plt.savefig(f"results/{voi}_data_availability.png")
    print(
        f"Figure with visualization of data availability over time for the chosen voivodeship saved in results/{voi}_data_availability.png"
    )
