from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "TSLA"
        # Assuming holding_status starts as False indicating no current position
        self.holding_status = False

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1min"  # Can be adjusted based on how frequently you want to check the price

    def run(self, data):
        allocation_dict = {}
        
        # Getting the latest close price for TSLA
        latest_close_price = data["ohlcv"][-1][self.ticker]["close"]

        # Checking conditions to buy or sell

        # If latest close price is >= 280 and we don't hold a position, set allocation to 1 (buy)
        if latest_close_price >= 280 and not self.holding_status:
            allocation_dict[self.ticker] = 1  # Indicates entering the position
            self.holding_status = True  # Updating holding status to True
        
        # If latest close price is < 280 and we hold a position, set allocation to 0 (sell)
        elif latest_close_price < 280 and self.holding_status:
            allocation_dict[self.ticker] = 0  # Indicates exiting the position
            self.holding_status = False  # Updating holding status to False

        # If conditions to buy or sell are not met, maintain current position
        else:
            allocation_dict[self.ticker] = 1 if self.holding_status else 0

        return TargetAllocation(allocation_dict)