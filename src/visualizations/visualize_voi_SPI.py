import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.SPI_utils import map_to_range


def visualize_voi_SPI(
    SPI_1: pd.DataFrame, SPI_3: pd.DataFrame, SPI_12: pd.DataFrame, voi: str
) -> None:
    """Visualization of SPIs over time for a particular voivodeship.

    Args:
        SPI_1 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one month for a particular voivodeship.
        SPI_3 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one quater for a particular voivodeship.
        SPI_12 (pd.DataFrame): Pandas DataFrame containing SPI calculated for one year for a particular voivodeship.
        voi (str): Name of the voivodeship.
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
            bbox_to_anchor=(0.68, 0.25, 0.5, 0.5),
        )
        ax[n].set(
            title=f"{spi_key} in time for the {voi} voivodeship",
            xlabel="Date",
            ylabel="SPI",
        )
        ax[n].grid(True)
        n += 1

    plt.suptitle(f"SPIs over time for the {voi} voivodeship", y=1, fontsize=16)
    plt.tight_layout()
    plt.savefig(f"results/SPI_in_time_{voi}.png", bbox_inches="tight")
    print(
        f"Figure with SPI over time for the {voi} voivodeship saved in results/SPI_in_time_{voi}.png"
    )
