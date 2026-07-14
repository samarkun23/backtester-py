from enum import Enum

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

@dataclass
class Order:
    symbol : str
    side: OrderSide
    order_type: OrderType
    quantity: float
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    take_profit: Option[float] = None
    stop_loss: Option[float] = None
    bar_index: int = 0
    order_id : int = 0

@dataclass
class Fill:
    order_id: int
    symbol: str
    side: OrderSide
    quantity: float
    fill_price: float
    commission: float
    bar_index: int  
    timestamp: datetime

class ExecutionSimulator:
    def __init__(self, spread_pips=0.2, commission_per_lost=3.5, pip_value=0.0001):
        self.spread_pips = spread_pips
        self.commission_per_lost = commission_per_lost
        self.pip_value = pip_value

    def create_order(self, symbol,side,quantity,order_type=OrderType.MARKET,limit_price=None,stop_price=None, take_profit=None, stop_loss=None,bar_index=0):
        # create and return an object 
        self.order_counter += 1
        return Order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            limit_price=limit_price,
            stop_price=stop_price,
            take_profit=take_profit,
            stop_loss=stop_loss,
            bar_index=bar_index,
            order_id=self.order_counter
        )

    def try_fill_market(self,order,next_bar_open,bar_index, timestamp):
        # Fill market order at next bar open + spread impact 
        if orde.side == OrderSide.BUY:
            fill_price = next_bar_open + self.spread
        else: 
            fill_price = next_bar_open - self.spread

        commission = self.commission_per_lost * order.quantity
        
        return Fill(
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            fill_price=fill_price,
            commission=commission,
            bar_index=bar_index,
            timestamp=timestamp
        )
    def check_stop_loss_take_profit(self,position,current_bar):
        high = current_bar['High']
        low = current_bar['Low']
        
        if position.stop_loss == OrderSide.BUY:
            if position.stop_loss and low <= position.stop_loss:
                return 'stop_loss', position.stop_loss
            if position.take_profit and high>= position.take_profit:
                return 'take_profit', position.take_profit
        else: # short position
            if position.stop_loss and high>= position.stop_loss:
                return 'stop_loss', position.stop_loss
            else:
                return 'take_profit', position.take_profit

        return None,None

    



