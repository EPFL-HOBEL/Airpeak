from sklearn.cluster import DBSCAN
from sklearn.preprocessing import RobustScaler
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def dbscan(df, timestamp, eps=0.01, ms=2, transformer=RobustScaler()):
    """
    Apply DBSCAN clustering algorithm to time series data grouped by date.
    This function processes time series data by applying DBSCAN clustering to identify groups
    of decay events. The data is first split by date and processed individually to make
    hyperparameter selection more universal.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing time series data with status labels
    timestamp : str
        Name of the timestamp column in the DataFrame
    eps : float, optional (default=0.01)
        The maximum distance between two samples for one to be considered as in the neighborhood of the other.
        This is the most important DBSCAN parameter to choose appropriately for your data set and distance function.
    ms : int, optional (default=2)
        The number of samples in a neighborhood for a point to be considered as a core point.
    transformer : sklearn.preprocessing object, optional (default=RobustScaler())
        Scaler to use for data preprocessing before DBSCAN clustering
    
    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the original data with an additional 'decay_group' column where:
        - -1 represents noise points or non-decay events
        - Other integers represent different decay event clusters
    
    Notes
    -----
    The function:
    1. Splits data by date
    2. Creates a cumulative sum of non-decay events
    3. Applies DBSCAN clustering on decay events (status_label=1)
    4. Merges results back with original data
    Any errors in processing a specific date are silently ignored (the function continues
    with the next date).
    """

    df_new = df.copy()
    df_new["Date"] = df_new[timestamp].dt.date
    date_list = df_new["Date"].unique()
    df_result = pd.DataFrame()

    for date in date_list:
        df_date = df_new.loc[df_new["Date"] == date]
        df_date["sum_nondecay"] = (df_date["status_label"] != 1).cumsum()
        df_working = df_date.loc[df_date["status_label"] == 1]

        try:
            X = df_working[["sum_nondecay"]]
            X_scaled = transformer.fit_transform(X)
            df_working["decay_group"] = DBSCAN(
                eps=eps, min_samples=ms, algorithm="ball_tree"
            ).fit_predict(X_scaled)
            df_date = df_date.merge(
                df_working[[timestamp, "decay_group"]], how="left", on=timestamp
            )
            df_result = pd.concat([df_result, df_date])
            df_result["decay_group"].fillna(-1, inplace=True)
        except Exception:
            continue

    return df_result
