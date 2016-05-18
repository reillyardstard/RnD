# -*- coding: utf-8 -*-
"""
Created on Thu May  5 00:20:10 2016

@author: jasonsmith
"""

import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas_datareader import data

class Bars(object):    
    def __init__(
        self, symbol
    ):
        self.symbol = symbol    
    
    def up_down_ratio(self):
        bars = data.get_data_yahoo(self.symbol, datetime.datetime(2015,1,1), datetime.datetime(2016,1,1))

        a = bars['Open']-bars['Close']
        n4 = a.mean()
        a = a.sub(n4)        
        n1 = a.abs().mean()
        n2 = a[a>=0].mean()
        n3 = a[a<0].abs().mean()
        return n1, n2, n3, n4

if __name__ == "__main__":
#    df = pd.DataFrame()    
    for symbol in ('aapl', 'bp', 'ibm'):    
        mybars = Bars(symbol)
        nos = mybars.up_down_ratio()
        print('')
        print(symbol)        
        print('Average bar size:  {:.6f}'.format(nos[0]))
        print('Average up move:   {:.6f}'.format(nos[1]))
        print('Average down move: {:.6f}'.format(nos[2]))
        
#        plt.plot
        