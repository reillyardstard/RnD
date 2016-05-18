# v.1.2
from __future__ import print_function
import sys
import pandas as pd
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
import time

class Historical:
    """
    Retrieves historical data from IB in a DataFrame and optionally writes to outfile
    Refer to https://www.interactivebrokers.co.uk/en/software/api/api.htm
    """
    
    def __init__(self, contract, date, t, bar_size='5 mins', duration='1 D', rth=1, outfile='none'):
        self.outfile = outfile
        self.headings = ['date', 'time', 'open', 'high', 'low', 'close', 'volume', 'count', 'WAP', 'hasGaps']
        self.bars = []       
        self.contract = contract
        self.date = date
        self.t = t
        self.bar_size = bar_size
        self.duration = duration
        self.rth = rth
        self.tick_id = 1
        self.con = ibConnection(host = 'localhost', port = 7496, clientId = 139)

        self.con.registerAll(self.all_msgs)
        self.con.register(self.incoming_bars, message.historicalData)
        self.con.connect(); time.sleep(1)
        end_datetime = ('%s %s US/Eastern' % (self.date, self.t))
        self.con.reqHistoricalData(tickerId=self.tick_id, contract=self.contract, endDateTime=end_datetime, 
                                   durationStr=self.duration, barSizeSetting=self.bar_size, 
                                   whatToShow='TRADES', useRTH=self.rth, formatDate=1)
        self.finished = False        
        while not self.finished:    # loop here until self._incoming_bars() finishes
            pass
        self.con.cancelHistoricalData(self.tick_id); time.sleep(1)
        self.con.disconnect(); time.sleep(1)
        self.bars = pd.DataFrame(self.bars, columns=self.headings)
        if self.outfile != 'none':
            self.bars.to_csv(self.outfile, cols=self.headings)

    def incoming_bars(self, msg):
        '''
        listener method receiving the historicalData msg from IB and building 
        a list one bar at a time
        '''
        if msg.date[:8] != 'finished':
            self.bars.append([msg.date[:8], msg.date[-8:], msg.open, msg.high, msg.low, msg.close, msg.volume, msg.count, msg.WAP, msg.hasGaps])
            print('.', end='')
        else:
            self.finished = True
            print('\n')

    def all_msgs(self, msg):
        '''
        listener method getting all messages from IB
        '''
        #print('Message from IB: {}, {}'.format(msg.typeName, msg))
        if(msg.typeName == 'historicalData'):  # handled by incoming_bars()
            pass
        else:
            #print('Message from IB: {}, {}'.format(msg.typeName, msg))
            pass    


def main():
    end_date = '20160301'
    end_time = '16:00:00'
    bar_size = '30 mins'
    duration = '1 M'
    rth = 1
    contract = Contract()
    contract.m_symbol = 'ES'
    contract.m_secType = 'FUT'
    contract.m_exchange = 'GLOBEX'
    contract.m_currency = 'USD'
    contract.m_expiry = '201606'
    outfile = '{}{}-{}-{}-{}.bars'.format(contract.m_symbol, contract.m_expiry, end_date, duration, bar_size).replace(' ','')

    print('{} (exp. {}) {} of {} bars ending {} {}'.format(contract.m_symbol, contract.m_expiry, duration, bar_size, end_date, end_time))
    print('File: {}'.format(outfile))

    hist = Historical(contract, end_date, end_time, bar_size, duration, rth, outfile)
    
    print(hist.bars.iloc[:3])    # print first and last three bars
    print(hist.bars.iloc[-3:])


if __name__ == "__main__":
    main()
