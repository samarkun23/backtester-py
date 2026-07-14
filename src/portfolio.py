from excution import OrderSide,Fill

class Position:
    def __init__(self,symbol,side,quantity,entry_price,entry_time,stop_loss=None,take_profit=None):
        self.symbol = symbol
        self.side = side
        self.quantity = quantity
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.is_open = True

