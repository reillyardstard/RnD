# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 22:23:09 2016

@author: jasonsmith
"""

# Download Apple price history and save adjusted close prices to numpy array
import pandas.io.data as pd
x = pd.DataReader("AAPL", "yahoo")['Adj Close']

# Make some trendlines
import trendy

print("# Generate general support/resistance trendlines and show the chart")
# window < 1 is considered a fraction of the length of the data set
trendy.gentrends(x, window = 1.0/3, charts = True)

'''n = 1.0
while n >= 0:
  print "window set to",n
  trendy.gentrends(x, window = n, charts = True)
  n = n - 0.2
'''

print("#Generate a series of support/resistance lines by segmenting the price history")
trendy.segtrends(x, segments = 2, charts = True)  # equivalent to gentrends with window of 1/2
trendy.segtrends(x, segments = 5, charts = True)  # plots several S/R lines

print("# Generate smaller support/resistance trendlines to frame price over smaller periods")
trendy.minitrends(x, window = 30, charts = True)

print("# Iteratively generate trading signals based on maxima/minima in given window")
trendy.iterlines(x, window = 1.0/4, charts = True)  # buy at green dots, sell at red dots

