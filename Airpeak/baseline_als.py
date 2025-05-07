from scipy import sparse
import numpy as np 


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