#Type code here
# For demonstration purposes, let's assume a mock exchange with placeholder functions

# Function to fetch the ticker data (mock implementation)
def fetch_ticker(symbol):
    # Placeholder implementation: return a random price
    import random
    return {'last': random.uniform(100, 200)}

# Function to create a market buy order (mock implementation)
def create_market_buy_order(symbol, asset_type, option_type, params):
    # Placeholder implementation: just print the order details
    print("Creating market buy order:", params)

# Function to fetch open positions (mock implementation)
def fetch_positions(symbol):
    # Placeholder implementation: return an empty list
    return []

# Function to create a market sell order (mock implementation)
def create_market_sell_order(symbol, asset_type, option_id):
    # Placeholder implementation: just print the order details
    print("Creating market sell order:", option_id)

# Set the symbol for QQQ options
symbol = 'QQQ/USD'

# Function to buy straddles
def buy_straddles():
    # Get the current stock price for QQQ
    ticker = fetch_ticker(symbol)
    stock_price = ticker['last']

    # Place an order to buy 10 straddles of QQQ expiring the next day at the money
    order = create_market_buy_order(symbol, 'option', 'straddle', {
        'amount': 10,
        'expiration': 'next_day',
        'strike': stock_price,
        'type': 'at_market'
    })

    print("Bought 10 straddles of QQQ:", order)

# Function to sell straddles for a profit
def sell_straddles_for_profit():
    # Get open positions for QQQ options
    positions = fetch_positions(symbol)

    # Loop through open positions
    for position in positions:
        # Check if the position is a straddle
        if position['type'] == 'straddle':
            # Calculate profit threshold (0.3 cents profit)
            profit_threshold = position['cost'] + 0.03

            # Check if profit threshold is reached
            if position['pnl'] >= profit_threshold:
                # Place sell order
                sell_order = create_market_sell_order(symbol, 'option', position['id'])
                print("Sold straddle for a 0.3 cents profit:", sell_order)

# Main function to execute the strategy
def main():
    while True:
        # Buy straddles
        buy_straddles()

        # Check for profit and sell
        sell_straddles_for_profit()

# Execute the main function
if __name__ == "__main__":
    main()