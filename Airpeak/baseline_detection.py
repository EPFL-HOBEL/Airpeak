import numpy as np
from scipy import sparse


def baseline_als(y, lam, p, niter=10):                                                                        

    s  = len(y)                                                                                               
    # assemble difference matrix                                                                              
    D0 = sparse.eye( s )                                                                                      
    d1 = [np.ones( s-1 ) * -2]                                                                             
    D1 = sparse.diags( d1, [-1] )                                                                             
    d2 = [ np.ones( s-2 ) * 1]                                                                             
    D2 = sparse.diags( d2, [-2] )                                                                             

    D  = D0 + D2 + D1                                                                                         
    w  = np.ones( s )                                                                                         
    for i in range( niter ):                                                                                  
        W = sparse.diags( [w], [0] )                                                                          
        Z =  W + lam*D.dot( D.transpose() )                                                                   
        z = sparse.linalg.spsolve( Z, w*y )                                                                                 
        w = p * (y > z) + (1-p) * (y < z)                                                                     

    return z



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
def baseline_detection(df, pollutant, base_lambda = 1e6, base_p =0.001):
    df_new = df.copy()
    arrary = np.hstack(([df.iloc[0][pollutant]]*100000, df[pollutant],[df.iloc[-1][pollutant]]*100000)) #add a long head and tail to help the algorithm
    df_new['baseline'] = baseline_als(arrary, base_lambda, base_p, niter=100)[100000:-100000] #drop the added values
    return df_new
