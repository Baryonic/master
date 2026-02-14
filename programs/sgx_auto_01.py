import requests # type: ignore
import pandas as pd # type: ignore
from tabulate import tabulate # type: ignore

# Function to read the API key from an external file
def get_api_key(file_path="config.txt"):
    try:
        with open(file_path, "r") as file:
            api_key = file.read().strip()
        return api_key
    except FileNotFoundError:
        print("Error: API key file not found!")
        return None

# Function to test the Alpha Vantage API
def test_api():
    api_key = get_api_key()
    if not api_key:
        print("Unable to proceed without an API key.")
        return

    url = "https://www.alphavantage.co/query"
    parameters = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": "MSFT",  # Replace with an SGX-compatible stock ticker if available
        "interval": "5min",
        "apikey": api_key
    }

    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant information
        try:
            if "Time Series (5min)" in data:
                time_series = data["Time Series (5min)"]
                latest_timestamp = list(time_series.keys())[0]
                latest_data = time_series[latest_timestamp]
                
                # Display latest stock data
                print("\nLatest Stock Data:")
                print("Stock: Microsoft Corporation (MSFT)")  # Adjust stock name if using SGX
                print(f"Timestamp: {latest_timestamp}")
                print(f"Open Price: {latest_data['1. open']}")
                print(f"High Price: {latest_data['2. high']}")
                print(f"Low Price: {latest_data['3. low']}")
                print(f"Close Price: {latest_data['4. close']}")
                print(f"Volume: {latest_data['5. volume']}")
            else:
                print("The expected structure was not found! Displaying raw data:")
                print_raw_data(data)
        except KeyError:
            print("Unexpected data structure received! Displaying raw data:")
            print_raw_data(data)
    else:
        print(f"API request failed! Status code: {response.status_code}")

# New Function: Print Raw Data
def print_raw_data(data):
    """
    Prints the raw API response data for debugging purposes.
    """
    print("\nRaw Data:")
    print(data)  # Outputs the raw JSON data to the console

# New Function to Display General Stats for SGX
def display_sgx_stats():
    api_key = get_api_key()
    if not api_key:
        print("Unable to proceed without an API key.")
        return

    url = "https://www.alphavantage.co/query"
    parameters = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": "SGX:S68",  # Replace with your preferred SGX-listed stock symbol
        "interval": "5min",
        "apikey": api_key
    }

    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant information
        try:
            time_series = data["Time Series (5min)"]
            df = pd.DataFrame.from_dict(time_series, orient="index")
            df = df.astype(float)  # Convert data to numeric format
            
            # Calculate mean values
            mean_open = df["1. open"].mean()
            mean_close = df["4. close"].mean()
            mean_volume = df["5. volume"].mean()

            print("\nGeneral Stats for Singapore Exchange Limited (SGX):")
            print(f"Average Open Price: {mean_open:.2f}")
            print(f"Average Close Price: {mean_close:.2f}")
            print(f"Average Trading Volume: {mean_volume:.0f}")
        except KeyError:
            print("Unexpected data structure received from the API!")
            print(data)
    else:
        print(f"API request failed! Status code: {response.status_code}")

def fetch_popular_symbols():
    api_key = get_api_key()
    if not api_key:
        print("Error: Unable to retrieve API key. Please check your configuration.")
        return

    # Pre-defined list of 50 popular symbols (modify as needed)
    popular_symbols = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK.B", "JPM", "V",
        "UNH", "JNJ", "XOM", "WMT", "PG", "HD", "MA", "CVX", "ABBV", "BAC",
        "PFE", "KO", "PEP", "COST"
    ]

    symbol_data = []
    for symbol in popular_symbols:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if "Global Quote" in data:
                quote = data["Global Quote"]
                symbol_data.append({
                    "Symbol": quote.get("01. symbol", symbol),
                    "Price": quote.get("05. price", "N/A"),
                    "Change (%)": quote.get("10. change percent", "N/A"),
                    "Volume": quote.get("06. volume", "N/A"),
                    "Trading Day": quote.get("07. latest trading day", "N/A")
                })
            else:
                print(f"Warning: No data found for symbol {symbol}.")
        else:
            print(f"Error: API request failed for symbol {symbol}. Status code {response.status_code}.")

    # Format and display the data as a table
    print(tabulate(symbol_data, headers="keys", tablefmt="grid"))


# Function to end the program
def end_program():
    print("Ending the program. Goodbye!")
    exit()

# Main function to display the menu and handle user input
def main():
    while True:
        print("\n\033[37m=== \033[94mSGX Auto Menu \033[37m=== \033[36mkeyday electronics \033[37m")
        print("1. Test Alpha Vantage API")
        print("2. Print Raw SGX Data")
        print("3. Display SGX stats")
        print("4. Ask symbols")
        print("99. End Program")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            test_api()
        elif choice == "2":
            # Call the test API function but ensure raw data is shown if needed
            api_key = get_api_key()
            if api_key:
                url = "https://www.alphavantage.co/query"
                parameters = {
                    "function": "TIME_SERIES_INTRADAY",
                    "symbol": "MSFT",  # Replace with your desired SGX stock
                    "interval": "5min",
                    "apikey": api_key
                }
                response = requests.get(url, params=parameters)
                data = response.json()
                print_raw_data(data)
            else:
                print("Unable to retrieve API key. Please check your configuration.")
        elif choice == "3":
            display_sgx_stats()
        elif choice == "4":
            fetch_popular_symbols()
        elif choice == "99":
            end_program()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
