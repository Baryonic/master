#!/usr/bin/env python3
import sys
import os

# Add libs to path to import secrets_manager
sys.path.append(os.path.join(os.path.expanduser("~"), "master", "libs"))
try:
    import secrets_manager
except ImportError:
    print("Error: Could not import secrets_manager.")
    sys.exit(1)

import alpaca_trade_api as tradeapi
import datetime
import requests
import time
import matplotlib.pyplot as plt
import numpy as np


API_KEY = secrets_manager.get_secret("alpaca.key")
API_SECRET = secrets_manager.get_secret("alpaca.secret")
BASE_URL = 'https://api.alpaca.markets'
DATA_URL = 'https://data.alpaca.markets/v1beta1/crypto'
headers = {
    'Apca-Api-Key-Id': API_KEY,
    'Apca-Api-Secret-Key': API_SECRET
}
api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL)

#account info
account = api.get_account()


def main():
    a=input('hit enter to \033[32mcontinue')
    menuoption=input(f"""\033[40m
\033[97m_____________________________________________________________________________    
\033[97m                                                                             |
\033[97m                                                                             |
        \033[95mMENU___(select one option)\033[97m                                           |
\033[97m                                                                             |
\033[97m_____________________________________________________________________________|                                    
\033[32m    1. print_position_market_value() 
\033[32m    2. accounrestriction() 
\033[32m    3. place_confimed_order() 
\033[33m    4. get_btc_available_to_sell() o? CHECK 11.
\033[32m    5. place_confirmed_order()
\033[31m    6. check_orders()  X
\033[31m    7. buy_and_hodl_strategy()
\033[33m    8. get_btc_price() o can fit in 17
\033[33m    9. get_balance() o checks dollars available can fit in 17
\033[31m    10. buy_low_sell_high()
\033[91m    11. sell_high_buy_low() ~X        
\033[33m    12. get_btc_balance() o can fit in 17.
\033[33m    13. get_open_sell_orders() ~too much info         
\033[33m    14. get_open_buy_orders()  ~too much info  
\033[32m    15. print_all_orders() 
\033[32m    16. fetch_and_plot() 
\033[33m    17. print_account_info() ~
\033[32m    18. calculate_open_orders()
\033[97m    99.EXIT                                                                                                                                                                       
\033[97m_______________________________________________________________________________                     
\033[36m    """)
    menu(menuoption)

def menu(x):
    if x == '1':
        return print_position_market_value()
    elif x == '2':
        return accountrestriction()
    elif x == '3':
        return place_confirmed_order()
    elif x == '4':
        return get_btc_available_to_sell()
    elif x == '5':
        return place_confirmed_order()
    elif x == '6':
        return check_orders()
    elif x == '7':
        return buy_and_hodl_strategy()
    elif x == '8':
        btc_price = get_btc_price()
        if btc_price is None:
            print("Failed to get BTC price. Exiting...")
        return print(f'ALPACA 1BTC = {get_btc_price()}$')
    elif x == '9':
        return print(f'balance = {get_balance()}___cash:{api.get_account().cash}')
    elif x == '10':
        return buy_low_sell_high()
    elif x == '11':
        return sell_high_buy_low()
    elif x == '12':
        return print(f'btc balance = {get_btc_balance()}')
    elif x == '13':
        return print(f'{print(get_open_sell_orders())}')
    elif x == '14':
        return print(f'{print(get_open_buy_orders())}')
    elif x == '15':
        return print_all_orders()
    elif x == '16':
        return fetch_and_plot()
    elif x == '17':
        return print_account_info()
    elif x == '18':
        return calculate_open_orders()
    elif x == '19':
        return print('test')
    elif x == '20':
        return print('test')
    elif x == '21':
        return print('test')
    elif x == '22':
        return print('test')
    elif x == '23':
        return print('test')
    elif x == '24':
        return print('test')
    elif x == '25':
        return print('test')
    elif x == '26':
        return print('test')
    elif x == '27':
        return print('test')
    elif x == '99':
        print('end of program')
        sys.exit()
    else:
        return print('please enter valid option eg."1"  ')
        

#--------------------------------------------------------------------------------------
def print_position_market_value():
    # Get a list of all of our positions.
    portfolio = api.list_positions()
    # Print the market value for each position
    for position in portfolio:
        print(f"\033[97m{position.symbol}: Market Value: \033[32m${position.market_value}")

def accountrestriction():
    # Check if the account is restricted from trading
    if account.trading_blocked:
        print('Account is currently restricted from trading.')
    else:
        print(f'account.trading_blocked: {account.trading_blocked}')
    # Check available buying power
    print(f'${account.buying_power} is available as buying power.')

def place_order():#OBSOLETE
    # Ask the user whether they want to buy or sell BTC
    action = input("Do you want to buy or sell BTC? (buy/sell): ").lower()
    # Validate the action
    if action not in ['buy', 'sell']:
        print("Invalid action. Please enter 'buy' or 'sell'.")
        return
    # Ask the user for the quantity of BTC
    quantity = float(input("How much BTC do you want to " + action + "?: "))
    # Ask the user for the price
    price = float(input("At what price do you want to " + action + " BTC?: "))
    # Calculate the cost basis
    cost_basis = quantity * price
    # Check if the cost basis is greater than or equal to the minimum amount
    if cost_basis < 1:
        print("The total cost of the order must be at least $1. Please increase the quantity or the price.")
        return
    # Place the order
    try:
        order = api.submit_order(
            symbol='BTCUSD',  # Symbol for Bitcoin
            qty=str(quantity),     # Quantity of BTC
            side=action,      # Buy or Sell
            type='limit',     # Limit order
            limit_price=str(price),# Specified price
            time_in_force='gtc' # Good 'til canceled
        )
        print(f"Order submitted successfully: {order}")
    except Exception as e:
        print(f"An error occurred: {e}")
def get_btc_available_to_sell():
    try:
        # Get the position for BTC
        btc_position = api.get_position('BTCUSD')
        print(f"BTC available to sell: {btc_position.qty}")
    except tradeapi.rest.APIError as e:
        # If there's no position found for BTC, it will raise an error
        print(f"No BTC position found in your account or an error occurred: {e}")
def place_confirmed_order():
    # Ask the user whether they want to buy or sell BTC
    action = input("Do you want to buy or sell BTC? (buy/sell): ").lower()
    # Validate the action
    if action not in ['buy', 'sell']:
        print("Invalid action. Please enter 'buy' or 'sell'.")
        return
    # Ask the user for the price
    price = float(input(f"At what price do you want to {action} BTC?: "))
    # Calculate how much BTC equals $1 at the given price
    btc_amount_for_one_dollar = 1 / price
    print(f"At the price of ${price}, $1 is equal to {btc_amount_for_one_dollar} BTC.")
    # Ask the user for the quantity of BTC
    quantity = float(input(f"How much BTC do you want to {action}?: "))
    # Calculate the total transaction value
    total_value = quantity * price
    print(f"The total {action} order will be for {quantity} BTC at a price of ${price} per BTC, totaling ${total_value}.")
    # Ask for user confirmation
    confirmation = input("Do you want to proceed with this order? (yes/no): ").lower()
    if confirmation != 'yes':
        print("Order canceled.")
        return
    # Place the order
    try:
        order = api.submit_order(
            symbol='BTCUSD',  # Symbol for Bitcoin
            qty=str(quantity),     # Quantity of BTC
            side=action,      # Buy or Sell
            type='limit',     # Limit order
            limit_price=str(price),# Specified price
            time_in_force='gtc' # Good 'til canceled
        )
        print(f"\033[32mOrder submitted successfully: {order}")
    except Exception as e:
        print(f"\033[31mAn error occurred: {e}")

def check_orders():
    # Ask the user for the type of orders to check
    order_type = input("Enter 'open orders' to check open orders or 'closed orders' to check closed orders: ").lower()
    # Validate the input
    if order_type not in ['open orders', 'closed orders']:
        print("Invalid input. Please enter 'open orders' or 'closed orders'.")
        return
    # Ask the user for the number of orders to check
    num_orders = int(input("How many orders do you want to check?: "))
    # Get the orders based on the type
    if order_type == 'open orders':
        orders = api.list_orders(status='open', limit=num_orders)
    else:
        orders = api.list_orders(status='closed', limit=num_orders)
    # Display the order information
    for order in orders:
        # Truncate the timestamp to microseconds precision (6 digits)
        order_time_str = order.submitted_at.isoformat(timespec='microseconds')
        # Parse the string to a datetime object
        order_time = datetime.fromisoformat(order_time_str).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Type: {order.side.upper()}, Quantity: {order.qty}, Price: {order.limit_price}, Time Executed: {order_time}")
def buy_and_hodl_strategy():
    api = tradeapi.REST(API_KEY, API_SECRET, base_url=DATA_URL)
    # Ask the user for the strategy type
    strategy = input("Please enter the strategy you want to execute (buy and hodl): ").lower()
    if strategy == 'buy and hodl':
        # Fetch the current price of BTC
        headers = {
            'APCA-API-KEY-ID': API_KEY,
            'APCA-API-SECRET-KEY': API_SECRET
        }
        response = requests.get(f"{DATA_URL}/BTCUSD/trades/latest", headers=headers)
        if response.status_code != 200:
            print("Failed to fetch the latest trade for BTCUSD.")
            return
        btc_trade = response.json()
        current_price = btc_trade['trade']['p']
        print(f"The current price of BTC is: ${current_price}")
        # Ask the user for the amount of BTC they want to buy
        amount = input("Enter the amount of BTC you want to buy (in BTC or USD): ")
        # Determine if the amount is in BTC or USD
        if 'btc' in amount.lower():
            btc_amount = float(amount.lower().replace('btc', '').strip())
        else:
            btc_amount = float(amount) / current_price
        # Ask the user for the target sell percentage
        target_percentage = float(input("Enter the target sell percentage (e.g., 120 for 120%): "))
        # Calculate the target sell price
        target_price = current_price * (target_percentage / 100)
        # Ask for user confirmation
        confirmation = input(f"Confirm buy order of {btc_amount} BTC at ${current_price} and sell order at ${target_price}? (yes/no): ").lower()
        if confirmation == 'yes':
            # Place a buy order at the current price
            buy_order = api.submit_order(
                symbol='BTCUSD',
                qty=str(btc_amount),
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            # Place a sell order at the target price
            sell_order = api.submit_order(
                symbol='BTCUSD',
                qty=str(btc_amount),
                side='sell',
                type='limit',
                limit_price=str(target_price),
                time_in_force='gtc'
            )
            print("Buy and sell orders placed successfully.")
        else:
            print("Order canceled.")

def get_btc_price():
    try:
        barset = api.get_crypto_bars('BTC/USD', '1Min', limit=1).df
        btc_price = barset['close'].iloc[-1]
        return btc_price
    except Exception as e:
        print(f"Error fetching BTC price: {e}")
        return None

def place_order2(symbol, qty, side, order_type, time_in_force, limit_price=None):
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force,
            limit_price=limit_price
        )
        return order
    except tradeapi.rest.APIError as e:
        print(f"API error placing order: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error placing order: {e}")
        return None
    
def buy_low_sell_high():
    symbol = 'BTC/USD'
    btc_price = get_btc_price()
    print(f'1BTC = {get_btc_price()} $')
    confirm = input("Do you want to proceed with buying BTC? (yes/no): ").lower()
    if confirm != 'yes':
        print("Exiting...")
        return
    usd_balance = get_balance()
    if usd_balance is None:
        print("Failed to get USD balance. Exiting...")
        return
    print(f"Available USD balance: {usd_balance}")
    usd_to_spend = float(input("Enter the amount in USD to spend on BTC: "))
    if usd_to_spend > usd_balance:
        print("Insufficient USD balance!")
        return
    btc_qty = usd_to_spend / btc_price
    buy_order = place_order2(symbol, btc_qty, 'buy', 'market', 'gtc')
    if buy_order is None:
        print("Failed to place buy order. Exiting...")
        return
    print(f"Buy order placed: {buy_order}")
    while True:
        order_status = api.get_order(buy_order.id)
        if order_status.status == 'filled':
            print("Buy order filled!")
            break
        print("Waiting for buy order to be filled...")
        time.sleep(5)
    sell_price = btc_price * 1.05
    sell_order = place_order2(symbol, btc_qty, 'sell', 'limit', 'gtc', limit_price=str(sell_price))
    if sell_order is None:
        print("Failed to place sell order. Exiting...")
        return
    print(f"Sell order placed at 105% of the buy price: {sell_order}")

def get_balance():
    try:
        account = api.get_account()
        return float(account.cash)
    except tradeapi.rest.APIError as e:
        print(f"API error fetching account balance: {e}")
        print(f"Raw response: {e.response}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching account balance: {e}")
        return None
    
def get_btc_balance():
    try:
        account = api.get_account()
        btc_positions = api.list_positions()
        btc_balance = 0
        for position in btc_positions:
            if position.symbol == 'BTCUSD':
                btc_balance += float(position.qty)
        return btc_balance
    except tradeapi.rest.APIError as e:
        print(f"API error fetching BTC balance: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching BTC balance: {e}")
        return None
        
def get_open_sell_orders():
    try:
        open_orders = api.list_orders(status='open')
        open_sell_orders = [order for order in open_orders if order.side == 'sell']
        return open_sell_orders
    except tradeapi.rest.APIError as e:
        print(f"API error fetching open sell orders: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching open sell orders: {e}")
        return []
    
def get_open_buy_orders():
    try:
        open_orders = api.list_orders(status='open')
        open_buy_orders = [order for order in open_orders if order.side == 'buy']
        return open_buy_orders
    except tradeapi.rest.APIError as e:
        print(f"API error fetching open buy orders: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching open buy orders: {e}")
        return []
    
def place_order_2(symbol, qty, side, order_type, time_in_force, limit_price=None):
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force,
            limit_price=limit_price
        )
        return order
    except tradeapi.rest.APIError as e:
        print(f"API error placing order: {e}")
        print(f"Raw response: {e.response}")
        return None
    except Exception as e:
        print(f"Unexpected error placing order: {e}")
        return None
    
def sell_high_buy_low():
    symbol = 'BTCUSD'
    btc_price = get_btc_price()
    if btc_price is None:
        print("Failed to get BTC price. Exiting...")
        return
    print(f"Current BTC/USD price: {btc_price}")
    btc_per_usd = 1 / btc_price
    print(f"1 USD is equivalent to {btc_per_usd:.8f} BTC")
    confirm = input("Do you want to proceed with selling BTC? (yes/no): ").lower()
    if confirm != 'yes':
        print("Exiting...")
        return
    btc_balance = get_btc_balance()
    if btc_balance is None or btc_balance == 0:
        print("No BTC available to sell. Exiting...")
        return
    print(f"Available BTC balance: {btc_balance}")
    open_sell_orders = get_open_sell_orders()
    reserved_btc = sum(float(order.qty) for order in open_sell_orders)
    free_btc_balance = btc_balance - reserved_btc
    print(f"Free BTC balance available for selling: {free_btc_balance}")
    btc_qty_to_sell = float(input("Enter the quantity of BTC to sell: "))
    if btc_qty_to_sell > free_btc_balance:
        print("Insufficient BTC balance!")
        return
    usd_equivalent = btc_qty_to_sell * btc_price
    print(f"USD equivalent of the sell order: {usd_equivalent}")
    sell_order = place_order_2(symbol, btc_qty_to_sell, 'sell', 'market', 'gtc')
    if sell_order is None:
        print("Failed to place sell order. Exiting...")
        return
    print(f"Sell order placed: {sell_order}")
    while True:
        order_status = api.get_order(sell_order.id)
        if order_status.status == 'filled':
            print("Sell order filled!")
            break
        print("Waiting for sell order to be filled...")
        time.sleep(5)
    buy_price = btc_price * 0.95
    btc_qty_to_buy = usd_equivalent / buy_price
    buy_order = place_order_2(symbol, btc_qty_to_buy, 'buy', 'limit', 'gtc', limit_price=str(buy_price))
    if buy_order is None:
        print("Failed to place buy order. Exiting...")
        return
    print(f"Buy order placed at 95% of the sell price: {buy_order}")

def print_all_orders():
    orders = api.list_orders(status='all', limit=100)  # Fetch up to 100 orders
    for order in orders:
        order_type = 'buy' if order.side == 'buy' else 'sell'
        status = 'open' if order.status in ['new', 'partially_filled', 'accepted', 'pending_new'] else 'closed'
        amount = order.qty
        symbol = order.symbol
        date_opened = order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        date_closed = order.filled_at.strftime('%Y-%m-%d %H:%M:%S') if order.filled_at else 'N/A'
        if("Buy"==str(order_type.capitalize())):
            if("Open"==str(status.capitalize())):
                print(f"\033[97mType: \033[92m{order_type.capitalize()}, \033[96mStatus: \033[92m{status.capitalize()}, "
              f"\033[97mAmount: \033[92m{amount} {symbol}, \033[95mDate Opened: {date_opened}, \033[93mDate Closed: {date_closed}")
                print("")
            else:
                print(f"\033[97mType: \033[92m{order_type.capitalize()}, \033[96mStatus: \033[31m{status.capitalize()}, "
              f"\033[97mAmount: \033[92m{amount} {symbol}, \033[95mDate Opened: {date_opened}, \033[93mDate Closed: {date_closed}")
                print("")
        else:
            if("Open"==str(status.capitalize())):
                print(f"\033[97mType:\033[31m{order_type.capitalize()}, \033[96mStatus: \033[92m{status.capitalize()}, "
              f"\033[97mAmount: \033[92m{amount} {symbol}, \033[95mDate Opened: {date_opened}, \033[93mDate Closed: {date_closed}")
                print("")
            else:
                print(f"\033[97mType:\033[31m{order_type.capitalize()}, \033[96mStatus: \033[31m{status.capitalize()}, "
              f"\033[97mAmount: \033[92m{amount} {symbol}, \033[95mDate Opened: {date_opened}, \033[93mDate Closed: {date_closed}")
                print("")

def fetch_and_plot():
    api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')#this line is  almost a duplicate, investigar
    symbol = 'BTC/USD'
    end_date = datetime.date.today()
    time_ranges = {
    '1 Day': {'days': 1, 'timeframe': '5Min'},  # Fetching 5-minute bars
    '1 Week': {'days': 7, 'timeframe': '30Min'},  # Fetching 30-minute bars
    '1 Month': {'days': 30, 'timeframe': '1Hour'},  # Fetching 1-hour bars
    '6 Months': {'days': 182, 'timeframe': '1Day'},  # Fetching daily bars
    '1 Year': {'days': 365, 'timeframe': '1Day'},  # Fetching daily bars
    '2 Years': {'days': 730, 'timeframe': '1Day'},  # Fetching daily bars
    '3 Years': {'days': 1095, 'timeframe': '1Day'},  # Fetching daily bars
    '5 Years': {'days': 1825, 'timeframe': '1Day'}  # Fetching daily bars
    }
    # Create subplots in a 2x4 grid
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    for ax, (title, params) in zip(axes, time_ranges.items()):
        days = params['days']
        timeframe = params['timeframe']
        start_date = end_date - datetime.timedelta(days=days)
        # Fetch historical data
        try:
            bars = api.get_crypto_bars(symbol, timeframe, start=start_date.isoformat(), end=end_date.isoformat()).df
            if bars.empty:
                print(f"No data returned for range: {title}")
                continue
            # Filter the data for the required symbol
            bars['symbol'] = bars['symbol'].apply(lambda x: x.replace("/", ""))
            btc_bars = bars[bars['symbol'] == symbol.replace("/", "")]
            if btc_bars.empty:
                print(f"No data found for symbol: {symbol.replace('/', '')} in range: {title}")
                continue
            # Calculate the average sell price as the average of the close prices
            btc_bars['average_sell_price'] = btc_bars['close']
            # Plot the graph
            ax.plot(btc_bars.index, btc_bars['average_sell_price'], label='Average Sell Price', color='b')
            # Add regression line and calculate slope
            x = np.arange(len(btc_bars))
            y = btc_bars['average_sell_price'].values
            if len(x) > 1:
                coeffs = np.polyfit(x, y, deg=1)
                slope = coeffs[0]
                y_pred = np.polyval(coeffs, x)
                ax.plot(btc_bars.index, y_pred, label='Trend Line', color='r', linestyle='--')
                # Calculate the difference between the last known price and the regression line
                last_known_price = y[-1]
                last_regression_price = y_pred[-1]
                price_difference = last_known_price - last_regression_price
                # Annotate the difference on the plot
                ax.annotate(f'Diff: {price_difference:.2f}', xy=(btc_bars.index[-1], last_known_price),
                            xytext=(btc_bars.index[-1], last_known_price + price_difference),
                            arrowprops=dict(facecolor='black', shrink=0.05))
            ax.set_xlabel('Time')
            ax.set_ylabel('Average Sell Price (USD)')
            ax.set_title(f'BTC/USD Over {title} (Slope: {slope:.2f})')
            ax.legend()
            ax.grid(True)
        except Exception as e:
            print(f"Error fetching data for range: {title} - {e}")
    plt.tight_layout()
    plt.show()

def print_account_info():
    # Get account information
    account = api.get_account()
    
    # Print account information
    print(f"\033[97mRegT Buying Power: \033[32m{account.regt_buying_power}")
    print(f"\033[97mDay Trading Buying Power: \033[32m{account.daytrading_buying_power}")
    print(f"\033[97mEffective Buying Power: \033[32m{account.buying_power}")
    print(f"\033[97mCash: \033[32m{account.cash}")
    # Use getattr to safely access attributes
    withdrawable_cash = getattr(account, 'withdrawable_cash', 'Not Available')
    pending_transfer_out = getattr(account, 'pending_transfer_out', 'Not Available')
    held_ach_deposits = getattr(account, 'held_ach_deposits', 'Not Available')
    
    print(f"\033[97mCash Withdrawable: \033[31m{withdrawable_cash}")
    print(f"\033[97mPending Transfer Out: \033[31m{pending_transfer_out}")
    print(f"\033[97mHeld ACH Deposits: \033[31m{held_ach_deposits}")
    
    print(f"\033[97mPending Transfer In: \033[32m{account.pending_transfer_in}")
    print(f"\033[97mEquity: \033[32m{account.equity}")
    print(f"\033[97mLong Market Value: \033[32m{account.long_market_value}")
    print(f"\033[97mShort Market Value: \033[32m{account.short_market_value}")
    print(f"\033[97mPosition Market Value: \033[32m{account.portfolio_value}")
    print(f"\033[97mNon-Marginable Buying Power: \033[32m{account.non_marginable_buying_power}")
    print(f"\033[97mInitial Margin: \033[32m{account.initial_margin}")
    print(f"\033[97mMaintenance Margin: \033[32m{account.maintenance_margin}")
    print(f"\033[97mSMA: \033[32m{account.sma}")
    print(f"\033[97mAccrued Fees: \033[32m{account.accrued_fees}")
    print(f"\033[97mDay Trade Count: \033[32m{account.daytrade_count}")

def calculate_open_orders():
    # Fetch the current BTC price using the existing get_btc_price function
    btc_price = get_btc_price()
    if btc_price is None:
        print("Unable to fetch BTC price.")
        return

    # Fetch open orders
    open_orders = api.list_orders(status='open')

    # Initialize totals
    total_buy_usd = 0
    total_sell_btc = 0

    # Iterate through open orders and calculate totals
    for order in open_orders:
        if order.side == 'buy' and 'BTC' not in order.symbol:
            total_buy_usd += float(order.qty) * float(order.limit_price)
        elif order.side == 'sell' and 'BTC' in order.symbol:
            total_sell_btc += float(order.qty)

    # Calculate USD value of BTC in open sell orders
    total_sell_usd = total_sell_btc * btc_price

    # Use the get_btc_balance function to get the total BTC balance
    total_btc = get_btc_balance()
    if total_btc is None:
        print("Unable to fetch BTC balance.")
        return

    # Fetch account information for total USD balance
    account = api.get_account()
    total_usd = float(account.cash) + float(account.long_market_value)

    # Calculate remaining balances after open orders
    remaining_btc = total_btc - total_sell_btc
    remaining_usd = total_usd - total_buy_usd

    # Print the calculations
    print(f"Total amount in open buy orders (USD): **{total_buy_usd}**")
    print(f"Total amount in open sell orders (BTC): **{total_sell_btc}**")
    print(f"Total amount in open sell orders (USD): **{total_sell_usd}**")
    print(f"Remaining BTC after open sell orders: **{remaining_btc}**")
    print(f"Remaining USD after open buy orders: **{remaining_usd}**")


tru=True
while(tru):
    main()