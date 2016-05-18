# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 23:22:35 2016

@author: jasonsmith
"""

import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#from pandas.io.data import DataReader
from pandas_datareader import data, wb
    
def extrema(x, max = True, min = True, strict = False, withend = True):
    """
    This function will index the extrema of a given array x.
    
    Options:
        max		If true, will index maxima
        min		If true, will index minima
        strict	If true, will not index changes to zero gradient
        withend	If true, always include x[0] and x[-1]
	
    Returns: 
        extrema indicies and values
    """
    # This is the gradient
    dx = np.zeros(len(x))
    dx[1:] = np.diff(x)
    dx[0] = dx[1]
	
    # Clean up the gradient in order to pick out any change of sign
    dx = np.sign(dx)
	
    # define the threshold for whether to pick out changes to zero gradient
    threshold = 0
    if strict:
        threshold = 1
		
    # Second order diff to pick out the spikes
    d2x = np.diff(dx)
	
    if max and min:
        d2x = abs(d2x)
    elif max:
        d2x = -d2x
	
    # Take care of the two ends
    if withend:
        d2x[0] = 2
        d2x[-1] = 2
	
    # Sift out the list of extremas
    ind = np.nonzero(d2x > threshold)[0]
	
    return (ind, x[ind])

if __name__ == "__main__":

    symbol = 'bp'
    bars = data.get_data_yahoo(symbol, datetime.datetime(2015,1,1), datetime.datetime(2016,1,1))
   
    fig = plt.figure(figsize=(9,10))
    fig.patch.set_facecolor('white')
    ax1 = fig.add_subplot(111,  ylabel=symbol+' price in $')    

    ax1.plot(bars['High'], 'b-', lw=0.5)
    ax1.plot(bars['Low'], 'b-', lw=0.5)

    exi,exv = extrema(bars['High'], min=False)
    f = pd.DataFrame(exv, index=bars.index[exi])
    ax1.plot(f, 'go', markersize=3)

    exi,exv = extrema(bars['Low'], max=False)
    f = pd.DataFrame(exv, index=bars.index[exi])
    ax1.plot(f, 'ro', markersize=3)

    ''''exi,exv = extrema(bars['Close'])
    f = pd.DataFrame(exv, index=bars.index[exi])    
    fig = plt.figure(figsize=(4,6))
    fig.patch.set_facecolor('white')
    ax1 = fig.add_subplot(111,  ylabel=symbol+' price in $')    
    ax1.plot(bars['Close'], 'b-', lw=1.)
    ax1.plot(f, 'ro', markersize=3)'''

    fig.show()
    