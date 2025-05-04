from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import log
from datetime import datetime

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TSLA"]
        self.pivot = None
        self.original_pivot = None
        self.has_shifted_long_pivot = False
        self.has_shifted_short_pivot = False

    @property
    def interval(self):
        return "1min"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        # Ensuring data is available
        if "ohlcv" not in data or len(data["ohlcv"]) < 1:
            return TargetAllocation({})

        current_time = datetime.strptime(data["ohlcv"][-1]["TSLA"]["date"], "%H:%M").time()

        # Defining the trading window
        start_time = datetime.strptime("10:00", "%H:%M").time()
        end_time = datetime.strptime("15:59", "%H:%M").time()

        # Resetting strategy at the start of the day
        if current_time == start_time:
            self.pivot = data["ohlcv"][-1]["TSLA"]["close"]
            self.original_pivot = self.pivot

        # End-of-Day Cleanup 
        if current_time >= end_time:
            log("End-of-day cleanup, liquidating positions")
            # Assume we liquidate and reset pivots for simplicity; in a live scenario, actual liquidation commands would be sent
            self.pivot = None
            self.original_pivot = None
            self.has_shifted_long_pivot = False
            self.has_shifted_short_pivot = False
            return TargetAllocation({})

        # Continue only if within trading window
        if start_time <= current_time < end_time:
            current_price = data["ohlcv"][-1]["TSLA"]["close"]
            allocation = {}

            # Entry Signals
            if current_price >= self.pivot + 0.10 and not self.has_shifted_long_pivot:
                allocation["TSLA"] = 0.1  # Buying signal, allocation size is illustrative
                # Single Pivot Adjustment Long
                if current_price >= self.original_pivot + 1:
                    self.pivot += 1
                    self.has_shifted_long_pivot = True
            elif current_price <= self.pivot - 0.10 and not self.has_shifted_short_pivot:
                allocation["TSLA"] = -0.1  # Shorting signal, allocation size is illustrative
                # Single Pivot Adjustment Short
                if current_price <= self.original_pivot - 1:
                    self.pivot -= 1
                    self.has_shifted_short_pivot = True

            return TargetAllocation(allocation)

        # Default no-action case
        return TargetAllocation({})