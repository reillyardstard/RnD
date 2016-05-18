# plotly candlesticks
from plotly.tools import FigureFactory as FF
import plotly as py
#import plotly.graph_objs
from pandas_datareader import data as web
from datetime import datetime
py.offline.init_notebook_mode() # run at the start of every notebook

df = web.get_data_yahoo("aapl", datetime(2016,1,1), datetime(2016,5,1))
fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)
py.offline.plot(fig, validate=False, show_link=False)