import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.utils import map_column_names


def visualize_pairplot(df: pd.DataFrame, voi: str) -> None:
    """
    Function to generate a pairplot of the input DataFrame using Seaborn's pairplot function.
    It saves the generated plot to a file named '{voi}_precip_pairplot.png' in the 'results' directory.

    Args:
        df (pd.DataFrame): Input DataFrame.
        voi (str): Name of the voivodeship.

    Returns:
        None
    """
    df = df[df.columns.difference(['station_code'])]
    sns.pairplot(df)
    plt.suptitle(f"Precipitation data pairplot", x=0.5, y=1, fontsize=20)
    plt.get_current_fig_manager().set_window_title(f"Precipitation data pairplot")
    plt.savefig(f"results/{voi}_precip_pairplot.png")

    print(
        f"Figure with pairplot od precipitation data saved in results/{voi}_precip_pairplot.png"
    )

def visualize_distributions(df: pd.DataFrame, voi:str) -> None:
    """
    Function to generate histogram plots of precipitation and snow data in the input DataFrame.
    It saves the generated plot to a file named '{voi}_precip_histplots.png' in the 'results' directory.

    Args:
        df (pd.DataFrame): Input DataFrame.
        voi (str): Name of the voivodeship.

    Returns:
        None
    """
    precip_columns = df[['24h_precipitation_mm', 'snow_cover_cm']]

    cols = precip_columns.columns.to_list()
    mapped_cols = map_column_names(cols)
    fig, ax = plt.subplots(1,2,figsize=(15,8))
    ax = ax.flatten()

    for i in range(len(mapped_cols)):
        sns.histplot(df[cols[i]], ax=ax[i], bins=30, kde=True)
        ax[i].set(title=f'Distribution of {mapped_cols[i]}', ylabel='counts')
    plt.suptitle("Distributions of precipitation data", fontsize='xx-large')
    plt.savefig(f"results/{voi}_precip_histplots.png")

    print(
        f"Figure with histplots od precipitation data saved in results/{voi}_precip_histplots.png"
    )

def visualize_boxplots(df: pd.DataFrame, voi:str) -> None:
    """
    Function to generate boxplot plots of selected columns in the input DataFrame.
    It saves the generated plot to a file named '{voi}_precip_boxplots.png' in the 'results' directory.

    Args:
        df (pd.DataFrame): Input DataFrame.
        voi (str): Name of the voivodeship.

    Returns:
        None
    """
    cols = ['24h_precipitation_mm', 'snow_cover_cm']
    mapped_cols = map_column_names(cols)
    fig, ax = plt.subplots(1,2,figsize=(20,10))
    ax = ax.flatten()

    for i in range(len(mapped_cols)):
        sns.boxplot(df[cols[i]], ax=ax[i])
        ax[i].set(title=f'Boxplot visualization of {mapped_cols[i]}', ylabel='counts')
    plt.suptitle("Boxplots of precipitation data", fontsize='xx-large')
    plt.savefig(f"results/{voi}_precip_boxplots.png")

    print(
        f"Figure with boxplots of precipitation data saved in results/{voi}_precip_boxplots.png"
    )

def visualize_correlations(df: pd.DataFrame, voi:str) -> None:
    """
    Function tp generate a correlation heatmap of numeric features in the input DataFrame.
    It saves the generated plot to a file named '{voi}_precip_correlations.png' in the 'results' directory.

    Args:
        df (pd.DataFrame): Input DataFrame.
        voi (str): Name of the voivodeship.

    Returns:
        None
    """
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])
    numeric_columns = numeric_columns[numeric_columns.columns.difference(['station_code'])]
    correlation = numeric_columns.corr()
    plt.figure(figsize=(12,12))
    sns.heatmap(correlation, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1, annot=True)
    plt.title('Correlation heatmap of numerical significant features', fontsize='xx-large')
    plt.savefig(f"results/{voi}_precip_correlations.png")

    print(
        f"Figure with correlations of precipitation data saved in results/{voi}_precip_correlations.png"
    )

def visualize_monthly_data(df: pd.DataFrame, voi:str) -> None:
    """
    Function to generate line plots of monthly aggregated time series for selected columns
    in the input DataFrame. It saves the generated plot to a file named
    '{voi}_precip_monthly_time_series.png' in the 'results' directory.

    Args:
        df (pd.DataFrame): Input DataFrame.
        voi (str): Name of the voivodeship.

    Returns:
        None
    """
    cols = ['24h_precipitation_mm', 'snow_cover_cm']
    mapped_cols = map_column_names(cols)
    df_plot = df.copy()
    df_plot = df_plot[cols].resample('ME').mean()

    fig, ax = plt.subplots(1,1,figsize=(10, 6))
    ax_ = ax.twinx()
    axes = [ax, ax_]
    colors = ['orange', 'blue']
    for i,c in enumerate(mapped_cols):
        sns.lineplot(data=df_plot, x='date', y=cols[i], label=c, errorbar=None, ax=axes[i], color=colors[i])
        axes[i].set_ylabel(c)
        axes[i].set_ylim(0,15)
    
    ax.legend(loc='upper right')
    ax.legend(loc='upper left')

    plt.title(f'Monthly time series for {mapped_cols}')
    plt.xlabel('Date')
    plt.savefig(f"results/{voi}_precip_monthly_time_series.png")

    print(
        f"Figure with monthly aggregated time series of precipitation data saved in results/{voi}_precip_monthly_time_series.png"
    )

def visualize_with_hue(df: pd.DataFrame, voi:str, hue_column: str) -> None:
    """
    Function to generate boxplot and time series plots with the specified hue column
    as a grouping variable. It saves the generated plots to files named
    '{voi}_precip_boxplot_{hue_column}_data.png' and '{voi}_precip_time_series_{hue_column}_data.png'
    in the 'results' directory.

    Args:
        df (pd.DataFrame): Input DataFrame.
        voi (str): Name of the voivodeship.
        hue_column (str): Name of the column to use as hue.
    
    Returns:
        None
    """
    col = ['24h_precipitation_mm']
    x_ticks = [x for x in df[hue_column].unique()]

    df = df[~df.index.duplicated(keep='first')]

    fig, ax = plt.subplots(1, 1, figsize=(12,10))
    sns.boxplot(data=df, y=col[0], x=hue_column, ax=ax)

    if hue_column == "precip_type":
        h_col = "Precipitation type"
    elif hue_column == "station_name":
        h_col = "Station name"
    elif hue_column == "river":
        h_col = "River"

    ax.set_title(f'Distribution of Precipitation (mm) with {h_col} as hue')
    ax.set_xlabel(h_col)
    ax.set_ylabel('Precipitation (mm)')
    ax.set_xticks(ticks = range(len(x_ticks)), labels=x_ticks)
    ax.set_xticklabels(x_ticks, rotation = 45)

    plt.savefig(f"results/{voi}_precip_boxplot_{hue_column}_data.png")

    print(
        f"Figure with boxplots (with hue = {hue_column}) of precipitation data saved in results/{voi}_precip_boxplot_{hue_column}_data.png"
    )

    if hue_column == "precip_type":
        fig, ax = plt.subplots(1, 1, figsize=(15, 5))
        sns.lineplot(data=df, x='date', y=col[0],  ax=ax, errorbar=None, hue=hue_column, alpha=0.5)
        ax.set_ylim(0,75)
        ax.set_title(f'Time series of Precipitation (mm) with Precipitation type as hue')
        ax.set_ylabel('Precipitation (mm)')
        ax.set_xlabel('Date')
        ax.legend(loc='upper right', title="Precipitation type")
        
        plt.savefig(f"results/{voi}_precip_time_series_{hue_column}_data.png")

        print(
            f"Figure with time series (with hue = {hue_column}) of precipitation data saved in results/{voi}_precip_time_series_{hue_column}_data.png"
        )

def visualize_EDA(df: pd.DataFrame, voi:str) -> None:
    """
    Function to generate a set of EDA plots including pairplot, distributions, boxplots,
    correlations, monthly aggregated time series, and time series with hue. It saves the generated
    plots to files in the 'results' directory.

    Args:
        df (pd.DataFrame): Input DataFrame.
        voi (str): Name of the voivodeship.

    Returns:
        None
    """
    visualize_pairplot(df, voi)
    visualize_distributions(df, voi)
    visualize_boxplots(df, voi)
    visualize_correlations(df, voi)
    visualize_monthly_data(df, voi)
    visualize_with_hue(df, voi, 'station_name')
    visualize_with_hue(df, voi, 'river')
    visualize_with_hue(df, voi, 'precip_type')




