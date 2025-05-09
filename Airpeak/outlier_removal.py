from sklearn.neighbors import LocalOutlierFactor


def outlier_removal(df, pollutant, outlier_neighbors):
    """
    Remove outliers from a DataFrame using Local Outlier Factor (LOF) algorithm.

    This function applies the LOF algorithm to identify and remove outliers in a specified
    pollutant column, considering the temporal sequence of measurements through the index.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing the pollutant measurements
    pollutant : str
        Name of the column containing the pollutant data to check for outliers
    outlier_neighbors : int
        Number of neighbors to consider when determining if a point is an outlier

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with outliers removed, maintaining the same structure as the input
        DataFrame but excluding the identified outlier rows

    Notes
    -----
    The function uses both the temporal index and pollutant values to identify outliers.
    Points identified as outliers (labeled as -1 by LOF) are removed from the dataset.
    """
    df_new = df.copy()
    lof = LocalOutlierFactor(
        n_neighbors=outlier_neighbors
    )  # window size for checking outliers
    df_new["index"] = (
        df_new.index
    )  # index used to consider adjacent data, usually works, could be cleaner
    df_new["non_outlier"] = lof.fit_predict(df_new[["index", pollutant]])
    df_new = df_new[df_new["non_outlier"] == 1]
    df_new.drop(columns=["index", "non_outlier"], inplace=True)
    return df_new
