from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler  # for data normalization
from sklearn.preprocessing import QuantileTransformer  # for data normalization


"""
Performs K-means clustering on concentration data to identify elevated measurements.

This function applies K-means clustering algorithm with 2 clusters on the provided dataframe
using 'diff_ma' (moving average difference) and 'diff_gd_abs' (absolute gradient difference)
features. The data is normalized using both scaling and quantile transformation before clustering.

Parameters
----------
df : pandas.DataFrame
    Input dataframe containing columns 'diff_ma', 'diff_gd_abs', and 'diff'
scaler : sklearn.preprocessing object, optional
    Scaler for data normalization (default is MinMaxScaler())
transformer : sklearn.preprocessing object, optional
    Transformer for data distribution (default is QuantileTransformer())

Returns
-------
pandas.DataFrame
    A copy of input dataframe with an additional boolean column 'elevated' indicating
    cluster membership. True (1) indicates elevated measurements, False (0) indicates
    normal measurements.

Notes
-----
The cluster with the higher average concentration value is automatically labeled as
the 'elevated' cluster (1), while the other cluster is labeled as normal (0).
"""


def k_means_ele(df, scaler=MinMaxScaler(), transformer=QuantileTransformer()):
    df_new = df.copy()
    X = df_new[["diff_ma", "diff_gd_abs"]]
    X_scaled = scaler.fit_transform(transformer.fit_transform(X))
    df_new["elevated"] = KMeans(n_clusters=2).fit_predict(X_scaled)
    if (
        df_new.loc[df_new["elevated"] == 1, "diff"].mean()
        < df_new.loc[df_new["elevated"] == 0, "diff"].mean()
    ):
        df_new["elevated"] = abs(
            df_new["elevated"] - 1
        )  # consider the cluster with higher average concentration value as "elevated"
    return df_new
