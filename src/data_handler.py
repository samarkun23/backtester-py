
import pandas as pd
import numpy as np

class DataHandler:
    def  __init__(self, filepath, symbol='EURUSD'):
        self.symbol = symbol
        self.data = pd.read_csv('../data/EURUSD_H1.csv', index_col=0, parse_dates=True)
        self.data.set_index('DateTime', inplace=True)
        self.data.sort.index(inplace=True)

        #remove any NAN rows 
        self.data.dropna(inplace=True)
        
        self.current_index = 0
        self.total_bars = len(self.data)

    def reset(self):
        # reset iterator to start
        self.current_index = 0

    def get_next_bar(self):
        # Return next bar or None if there are no more bars means it's end
        if self.current_index >= self.total_bars:
            return None
        # return the dict with bar data + index data
        bar = self.data.iloc[self.current_index].to_dict()
        bar['timestamp'] = self.data.index[self.current_index]
        bar['bar_index'] = self.current_index
        self.current_index += 1
        return bar

    def get_data_until(self,index):
        # Get all the data up to current index (prevents looks ahead bias)
        return self.data.iloc[:index+1]

    def get_latest_bar(self,index=None):
        # get most recent bar for indication calculation
        if index in None:
            index = self.current_index + 1
        if index < 0:
            return None
        return self.data.iloc[index].to_dict()
    
    def __len__(self):
        return self.total_bars