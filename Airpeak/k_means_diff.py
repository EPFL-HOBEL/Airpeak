import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import QuantileTransformer

"""
    Performs K-means clustering on concentration gradient data to classify different states in time series.

    This function applies K-means clustering to identify different states (baseline, decay, buildup,
    and optionally plateau) in concentration gradient data. It processes elevated periods in the data
    and labels them according to their gradient characteristics.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing concentration gradient data
    timestamp : str
        Column name for timestamp values
    n_clusters : int, optional (default=2)
        Number of clusters for K-means (2 for no steady state, 3 for with steady state)
    scaler : sklearn.preprocessing object, optional (default=MinMaxScaler())
        Scaler object for data normalization
    transformer : sklearn.preprocessing object, optional (default=QuantileTransformer())
        Transformer object for data transformation

    Returns
    -------
    pandas.DataFrame
        DataFrame with added 'status_label' column indicating state classification:
        - 0: baseline (non-elevated periods)
        - 1: decay
        - 2: buildup (for n_clusters=2)
        - 2: plateau, 3: buildup (for n_clusters=3)

    Notes
    -----
    The function expects the input DataFrame to have 'elevated', 'diff_gd_ln', and 'diff_gd_abs'
    columns. The 'elevated' column should be binary (0/1) indicating elevated periods.
    """


def k_means_diff(
    df,
    timestamp,
    n_clusters=2,
    scaler=MinMaxScaler(),
    transformer=QuantileTransformer(),
):

    df_new = df.copy()
    df_peak = df_new.loc[df_new["elevated"] == 1]
    X = df_peak[["diff_gd_ln", "diff_gd_abs"]]
    X_scaled = scaler.fit_transform(transformer.fit_transform(X))
    df_peak["status"] = KMeans(n_clusters=n_clusters, max_iter=100000).fit_predict(
        X_scaled
    )
    # n_clusters of 2 if no steady state, otherwise 3
    label_dic = (
        df_peak.groupby("status").agg({"diff_gd": np.mean}).rank()["diff_gd"].to_dict()
    )  # ranking clusters by concentration gradient
    df_peak["status_label"] = df_peak["status"].map(label_dic)
    # 0-baseline, 1-decay, 2-buildup | 0-baseline, 1-decay, 2-pleateau, 3-buildup
    df_new = df_new.merge(
        df_peak[["status_label", timestamp]], how="left", on=timestamp
    )
    df_new["status_label"].fillna(0, inplace=True)  # 0 means non-decay
    return df_new
