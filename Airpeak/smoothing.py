from scipy import signal


def smoothing(df, pollutant, smoothing_window, smoothing_order):
    """
    Apply Savitzky-Golay filter to smooth pollutant data in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing pollutant measurements
    pollutant : str
        Name of the column containing pollutant data to be smoothed
    smoothing_window : int
        Length of the filter window (must be odd number and greater than smoothing_order)
    smoothing_order : int
        Order of the polynomial used to fit the samples

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with smoothed pollutant data

    Notes
    -----
    This step is optional. Consider applying it if the raw data is noisy. 
    Uses scipy.signal.savgol_filter for smoothing, which fits a polynomial of order
    'smoothing_order' to windows of size 'smoothing_window'.

    Example
    -------
    >>> smoothed_df = smoothing(df, "CO2", 5, 3)
    """
    df_new = df.copy()
    df_new[pollutant] = signal.savgol_filter(
        df_new[pollutant], smoothing_window, smoothing_order
    )
    return df_new
