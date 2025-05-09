import numpy as np

def feature_generation(df, pollutant, timestamp, diff_ma_window=5, diff_rhl_window=5):
    """
    Generate additional features from time series data of pollutant measurements.
    This function calculates several features based on the difference between pollutant
    measurements and their baseline values, including moving averages, gradients,
    and relative high-low metrics.
    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing pollutant measurements and baseline values
    pollutant : str
        Column name for the pollutant measurements
    timestamp : str
        Column name for the timestamp data
    diff_ma_window : int, optional
        Window size for moving average calculation (default is 5)
    diff_rhl_window : int, optional
        Window size for relative high-low calculation (default is 5)
    Returns
    -------
    pandas.DataFrame
        DataFrame with original data and additional features:
        - min_diff: time difference between measurements in minutes
        - diff: difference between pollutant and baseline
        - diff_ma: moving average of the difference
        - diff_gd: gradient of concentration difference
        - diff_gd_ln: natural log of concentration difference gradient
        - diff_gd_sign: binary indicator of positive/negative gradient
        - diff_gd_abs: absolute value of the gradient
        - diff_rhl: relative high-low metric
    Notes
    -----
    The function assumes input DataFrame contains 'baseline' column.
    Natural log transformation of negative values results in NaN, which are filled with 0.
    """
    
    df_new = df.copy()
    df_new["min_diff"] = (
        df_new[timestamp].diff().dt.total_seconds() / 60
    )  # calculate timestamp changes

    df_new["diff"] = (
        df_new[pollutant] - df_new["baseline"]
    )  # feature 1 difference relative to baseline
    df_new["diff_ma"] = (
        df_new["diff"].rolling(diff_ma_window, min_periods=1, center=True).mean()
    )  # moving average

    df_new["diff_gd"] = (
        df_new["diff_ma"].diff() / df_new["min_diff"]
    )  # feature 2 gradient of concentration difference

    df_new["diff_gd_ln"] = (
        np.log(df_new["diff_ma"]).diff() / df_new["min_diff"]
    )  # feature 3 concentration difference natural log
    df_new["diff_gd_ln"].fillna(
        value=0, inplace=True
    )  # if concentration lower than baseline, log(negative) generates NA

    df_new["diff_gd_sign"] = (df_new["diff_gd"] > 0).astype(
        int
    )  # feature 4 positive/negative sign

    df_new["diff_gd_abs"] = abs(
        df_new["diff_gd"]
    )  # feature 5 absolute value of the gradient

    df_new["diff_rhl"] = (
        df_new["diff"]
        - df_new["diff"].rolling(diff_rhl_window, min_periods=1, center=True).min()
    ) / (
        df_new["diff"].rolling(diff_rhl_window, min_periods=1, center=True).max()
        - df_new["diff"].rolling(diff_rhl_window, min_periods=1, center=True).min()
    )
    # feature 6 relative high-low

    return df_new
