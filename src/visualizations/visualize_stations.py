import geopandas as gpd
import matplotlib.pyplot as plt


def get_voivodeship_names() -> list:
    """Function to fetch and return a list of voivodeship names with spaces and
       dashes removed.

    Returns:
        list: A list containing unique names of voivodeships.
    """
    geojson = gpd.read_file(
        "https://simplemaps.com/static/svg/country/pl/admin1/pl.json"
    )
    geojson["name"] = (
        geojson["name"]
        .apply(lambda x: x.replace(" ", ""))
        .apply(lambda x: x.replace("-", ""))
    )
    voivodeships = geojson["name"].unique().tolist()
    return voivodeships


def visualize_stations(
    voi_polygon: gpd.GeoSeries, voi_gdf: gpd.GeoDataFrame, voi: str
) -> None:
    """Function to visualize stations within specific voivodeship

    Args:
        voi_polygon (gpd.GeoSeries): Polygon representing voivodeship borders
        voi_gdf (gpd.GeoDataFrame): GeoDataFrame containing stations data within
                                    the voivodeship
        voi (str): Name of the voivodeship

    Returns:
            None
    """
    ax = voi_polygon.plot(
        figsize=(10, 10), color="lightgrey", edgecolor="blue", label=voi
    )
    voi_gdf.plot(ax=ax, color="red", markersize=25)

    for x, y, label in zip(voi_gdf.geometry.x, voi_gdf.geometry.y, voi_gdf["name"]):
        ax.text(x, y, label, fontsize=7, ha="left")

    ax.set_xlim([min(voi_gdf.geometry.x) - 0.75, max(voi_gdf.geometry.x) + 0.75])
    ax.set_ylim([min(voi_gdf.geometry.y) - 0.75, max(voi_gdf.geometry.y) + 0.75])

    plt.title(f"Stations, Voivodeship - {voi}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.get_current_fig_manager().set_window_title(f"Stations, Voivodeship - {voi}")
    plt.savefig(f"results/{voi}_stations.png")
    print(
        f"Figure with visualization of stations within specific voivodeship saved in results/{voi}_stations.png"
    )
