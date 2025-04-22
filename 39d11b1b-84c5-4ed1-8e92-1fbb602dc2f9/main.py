from surmount import Strategy

class TslaPingPongStopLimitCushion(Strategy):
    def initialize(self):
        self.symbol     = "TSLA"
        self.buy_price  = 249.00
        self.sell_price = 248.00
        self.cushion    = 1.00             # $1 cushion for limit price
        # keep orders alive in pre‑ and after‑market
        self.order_kwargs = {"extended_hours": True}

    def on_market_data(self, snapshot):
        position    = self.get_position(self.symbol).quantity
        open_orders = self.get_open_orders(self.symbol)

        if position == 0:
            # Flat → cancel any stray SELLs, then ensure one BUY stop‑limit
            for o in open_orders:
                if o.side == "SELL":
                    self.cancel_order(o.id)

            if not any(
                o.side=="BUY" and 
                o.order_type=="STOP_LIMIT" and 
                o.stop_price==self.buy_price and 
                o.limit_price==self.buy_price + self.cushion
                for o in open_orders
            ):
                self.log(f"Placing BUY stop‑limit @ stop={self.buy_price} / limit={self.buy_price + self.cushion}")
                self.submit_order(
                    symbol      = self.symbol,
                    qty         = 1,
                    side        = "BUY",
                    order_type  = "STOP_LIMIT",
                    stop_price  = self.buy_price,
                    limit_price = self.buy_price + self.cushion,
                    time_in_force = "GTC",
                    **self.order_kwargs
                )

        else:
            # Long → cancel any stray BUYs, then ensure one SELL stop‑limit
            for o in open_orders:
                if o.side == "BUY":
                    self.cancel_order(o.id)

            if not any(
                o.side=="SELL" and 
                o.order_type=="STOP_LIMIT" and 
                o.stop_price==self.sell_price and 
                o.limit_price==self.sell_price - self.cushion
                for o in open_orders
            ):
                self.log(f"Placing SELL stop‑limit @ stop={self.sell_price} / limit={self.sell_price - self.cushion}")
                self.submit_order(
                    symbol       = self.symbol,
                    qty          = position,
                    side         = "SELL",
                    order_type   = "STOP_LIMIT",
                    stop_price   = self.sell_price,
                    limit_price  = self.sell_price - self.cushion,
                    time_in_force = "GTC",
                    **self.order_kwargs
                )