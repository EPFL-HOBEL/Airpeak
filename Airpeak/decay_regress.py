from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def decay_regress(df_date, pollutant, timestamp, portion=[0, 1]):
    """
    Performs linear regression analysis on decay periods in time series data.

    This function analyzes identified decay periods in environmental data, calculating decay rates
    and associated statistics through linear regression of log-transformed concentrations.

    Parameters
    ----------
    df_date : pandas.DataFrame
        DataFrame containing the time series data with decay periods identified
    pollutant : str
        Name of the column containing pollutant concentrations
    timestamp : str
        Name of the column containing timestamp data
    portion : list of float, optional
        Two elements list specifying the start and end portions of each decay period to use
        [start_fraction, end_fraction], default [0,1] uses entire periods

    Returns
    -------
    pandas.DataFrame
        DataFrame containing regression results with columns:
        - pollutant: name of analyzed pollutant
        - time: midpoint time of decay period
        - decay_start: start time of decay period
        - decay_end: end time of decay period
        - decay_rate: calculated decay rate coefficient
        - r2: R-squared value of regression
        - ste: standard error of regression
        - num_of_point: number of points in regression
        - base_value: baseline concentration at start
        - median_ele: median concentration above baseline
        - max_diff: maximum concentration difference
        - group: decay period identifier
        - method: analysis method identifier ('decay')

    Notes
    -----
    - Requires decay periods to be pre-identified in 'decay_group' column
    - Performs log-linear regression on concentration differences from baseline
    - Excludes decay periods with fewer than 3 points
    - Uses natural logarithm for decay rate calculation
    """

    decay_result = []
    decay_list = [
        i for i in set(df_date["decay_group"]) if i >= 0
    ]  # unique decay groups excluding 0 (non-decay)
    for decay in decay_list:
        df_regress = df_date[df_date["decay_group"] == decay]
        df_regress = df_regress[
            int(len(df_regress) * portion[0]) : int(len(df_regress) * portion[1])
        ]  ## remove heads and tails
        num = len(df_regress)
        init = df_regress[pollutant].iloc[0]
        t_init = df_regress[timestamp].iloc[0]
        t_end = df_regress[timestamp].iloc[-1]
        t_mid = df_regress[timestamp].iloc[round(num / 2)]
        base_init = df_regress["baseline"].iloc[0]
        df_regress["ln"] = -1 * np.log(
            (df_regress[pollutant] - df_regress["baseline"]) / (init - base_init)
        )
        df_regress["t_diff"] = (
            (df_regress[timestamp] - t_init) / np.timedelta64(1, "s") / 3600
        )
        df_regress = df_regress.dropna(
            subset=[pollutant, "diff", "diff_ma", "diff_gd", "diff_rhl"]
        )
        if num < 3:  # at least 3 points to run regression
            continue
        y = df_regress["ln"]
        x = np.array(df_regress["t_diff"]).reshape(-1, 1)
        lr = LinearRegression().fit(x, y)
        y_pred = lr.predict(x)
        coef = lr.coef_[0]
        r_squared = 1 - (float(sum((y - y_pred) ** 2))) / sum((y - np.mean(y)) ** 2)
        residuals = (y - y_pred) ** 2
        standard_error = (sum(residuals) / (num - 2)) ** 0.5
        median = (df_regress[pollutant] - df_regress["baseline"]).median()
        maximum = df_regress.iloc[-1][pollutant] - df_regress.iloc[0][pollutant]
        decay_result.append(
            {
                "pollutant": pollutant,
                "time": t_mid,
                "decay_start": t_init,
                "decay_end": t_end,
                "decay_rate": coef,
                "r2": r_squared,
                "ste": standard_error,
                "num_of_point": num,
                "base_value": base_init,
                "median_ele": median,
                "max_diff": maximum,
                "group": decay,
                "method": "decay",
            }
        )

    decay_result = pd.DataFrame(decay_result)
    return decay_result
