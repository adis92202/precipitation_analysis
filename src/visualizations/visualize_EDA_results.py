import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def visualize_pairplot(df: pd.DataFrame, voi:str) -> None:
    """
    Function to generate a pairplot of the input DataFrame using Seaborn's pairplot function.
    It saves the generated plot to a file named '{voi}_precip_pairplot.png' in the 'results' directory.

    Args:
        df (pd.DataFrame): Input DataFrame.
        voi (str): Name of the voivodeship.

    Returns:
        None
    """
    sns.pairplot(df)
    plt.title(f"Precipitation data pairplot")
    plt.get_current_fig_manager().set_window_title(f"Precipitation data pairplot")
    plt.savefig(f"results/{voi}_precip_pairplot.png")

    print(
        f"Figure with pairplot od precipitation data saved in results/{voi}_precip_pairplot.png"
    )

def visualize_distributions(df: pd.DataFrame, voi:str) -> None:
    """
    Function to generate histogram plots of numeric columns in the input DataFrame.
    It saves the generated plot to a file named '{voi}_precip_histplots.png' in the 'results' directory.

    Args:
        df (pd.DataFrame): Input DataFrame.
        voi (str): Name of the voivodeship.

    Returns:
        None
    """
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])

    cols = numeric_columns.columns.to_list()
    fig, ax = plt.subplots(2,3,figsize=(20,10))
    ax = ax.flatten()

    for i in range(len(cols)):
        sns.histplot(df[cols[i]], ax=ax[i], bins=30, kde=True)
        ax[i].set(title=f'Histplot {cols[i]}', ylabel='counts')

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
    fig, ax = plt.subplots(1,2,figsize=(20,10))
    ax = ax.flatten()

    for i in range(len(cols)):
        sns.boxplot(df[cols[i]], ax=ax[i])
        ax[i].set(title=f'Boxplot {cols[i]}', ylabel='counts')

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
    correlation = numeric_columns.corr()
    plt.figure(figsize=(12,12))
    sns.heatmap(correlation, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1, annot=True)
    plt.title('Correlation heatmap of numerical features')
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
    df_plot = df.copy()
    df_plot = df_plot[cols].resample('ME').mean()

    plt.figure(figsize=(10, 6))
    for c in cols:
        sns.lineplot(data=df_plot, x='date', y=c, label=c, errorbar=None)

    plt.title(f'Time series for {cols}')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend(title='Parameter')
    plt.savefig(f"results/{voi}_precip_monthly_time_series.png")

    print(
        f"Figure with monthly aggregated time series of precipitation data saved in results/{voi}_precip_monthly_time_series.png"
    )

def visualize_with_hue(df: pd.DataFrame, voi:str, hue_column: str) -> None:
    """
    Function to generate boxplot and time series plots with the specified hue column
    as a grouping variable. It saves the generated plots to files named
    '{voi}_precip_boxplots_{hue_column}_data.png' and '{voi}_precip_time_series_{hue_column}_data.png'
    in the 'results' directory.

    Args:
        df (pd.DataFrame): Input DataFrame.
        hue_column (str): Name of the column to use as hue.
        voi (str): Name of the voivodeship.

    Returns:
        None
    """
    cols = ['24h_precipitation_mm', 'snow_cover_cm']
    x_ticks = [x for x in df[hue_column].unique()]

    fig, ax = plt.subplots(1, 2, figsize=(15,10))

    for i, column in enumerate(cols):   
        sns.boxplot(data=df, y=column, x=hue_column, ax=ax[i])
        ax[i].set_title(f'Distribution of {column} with {hue_column} as hue')
        ax[i].set_xticklabels(x_ticks, rotation = 50)
        
    plt.savefig(f"results/{voi}_precip_boxplots_{hue_column}_data.png")

    fig, ax = plt.subplots(2, 1, figsize=(15, 12))
    for i, column in enumerate(cols):
        sns.lineplot(data=df, x='date', y=column,  ax=ax[i], errorbar=None, hue=hue_column)
        ax[i].set_title(f'Time series of {column} with {hue_column} as hue')
        ax[i].set_ylabel(column)
        ax[i].set_xlabel('Rok')
        ax[i].legend(loc='upper right', title=hue_column)
 
    plt.savefig(f"results/{voi}_precip_time_series_{hue_column}_data.png")

    print(
        f"Figure with boxplots and time series (with hue = {hue_column}) of precipitation data saved in results/{voi}_precip_boxplots_{hue_column}_data.png and results/{voi}_precip_time_series_{hue_column}_data.png"
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
    visualize_with_hue(df, voi, 'SMDB_status')
    



