import numpy as np
from scipy import sparse



def baseline_als(y, lam, p, niter=10):
    """
    Asymmetric Least Squares Smoothing for baseline correction.

    This function implements baseline correction using asymmetric least squares smoothing.
    The algorithm iteratively improves a fit of the baseline by applying weights to points
    above or below the current baseline estimate.

    Parameters
    ----------
    y : array_like
        Input signal, 1-D array
    lam : float
        Lambda parameter controls the smoothness of the baseline.
        Larger values make the baseline more smooth.
    p : float
        Asymmetry parameter between 0 and 1. Values greater than 0.5 penalize peaks more than valleys.
        p=0.5 gives symmetric least squares smoothing.
    niter : int, optional
        Number of iterations for the baseline estimation. Default is 10.

    Returns
    -------
    z : ndarray
        The estimated baseline

    Notes
    -----
    The algorithm is based on P. Eilers and H. Boelens work in 2005
    "Baseline Correction with Asymmetric Least Squares Smoothing"

    References
    ----------
    Eilers, P., Boelens, H. (2005). Baseline Correction with Asymmetric Least Squares Smoothing.
    """
    s = len(y)
    # assemble difference matrix
    D0 = sparse.eye(s)
    d1 = [np.ones(s - 1) * -2]
    D1 = sparse.diags(d1, [-1])
    d2 = [np.ones(s - 2) * 1]
    D2 = sparse.diags(d2, [-2])

    D = D0 + D2 + D1
    w = np.ones(s)
    for i in range(niter):
        W = sparse.diags([w], [0])
        Z = W + lam * D.dot(D.transpose())
        z = sparse.linalg.spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)

    return z



def baseline_detection(df, pollutant, base_lambda=1e6, base_p=0.001):
    """
    Detects baseline in pollutant measurement data using Asymmetric Least Squares smoothing.

    This function processes a DataFrame containing pollutant measurements and calculates
    the baseline signal using the baseline_als algorithm. It adds padding to the beginning
    and end of the data to improve edge detection.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing pollutant measurements
    pollutant : str
        Column name in the DataFrame containing the pollutant measurements
    base_lambda : float, optional
        Smoothing parameter for baseline_als algorithm (default is 1e6)
    base_p : float, optional
        Asymmetry parameter for baseline_als algorithm (default is 0.001)

    Returns
    -------
    pandas.DataFrame
        A copy of the input DataFrame with an additional 'baseline' column containing
        the calculated baseline values

    Notes
    -----
    The function adds padding (100000 points) at the beginning and end of the data
    to improve baseline detection at the edges. These padding points are removed
    from the final output.
    """

    df_new = df.copy()
    arrayr = np.hstack(
        (
            [df.iloc[0][pollutant]] * 100000,
            df[pollutant],
            [df.iloc[-1][pollutant]] * 100000,
        )
    )  # add a long head and tail to help the algorithm
    df_new["baseline"] = baseline_als(arrayr, base_lambda, base_p, niter=100)[
        100000:-100000
    ]  # drop the added values
    return df_new
