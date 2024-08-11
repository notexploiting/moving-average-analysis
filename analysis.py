import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Import the data (replace the first parameter with any .csv stock data)
data = pd.read_csv('NVDA_stock_data.csv', index_col='Date', parse_dates=True)

# Calculate Simple Moving Averages
data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()

# Calculate Buy Signals
data['Buy_Signal'] = (data['Close'] > data['SMA_20']) & (data['Close'].shift(1) <= data['SMA_20'].shift(1))

# Calculate Daily Returns and Rolling Volatility
data['Daily_Return'] = data['Close'].pct_change()
data['Rolling_Volatility'] = data['Daily_Return'].rolling(window=20).std()

# Calculate Relative Strength Index
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
data['RSI'] = calculate_rsi(data)

# Plot everything together
plt.figure(figsize=(14, 8))

# Formatter for the date
months = mdates.MonthLocator()
days = mdates.DayLocator()
time_format = mdates.DateFormatter('%Y %b %d') # e.g. 2023 Jan 12

# Subplot 1: Closing Price, Simple Moving Averages, and Buy Signals
plt.subplot(4, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue', alpha=0.3)
plt.plot(data['SMA_20'], label='20-Day SMA', color='red', alpha=0.6)
plt.plot(data['SMA_50'], label='50-Day SMA', color='green', alpha=0.6)
buy_signals = data[data['Buy_Signal']] # When price crosses above the 20-day SMA
plt.scatter(buy_signals.index, buy_signals['Close'], marker='o', color='green', s=50, label='Buy Signal', edgecolors='k')
plt.title('Stock Price and Moving Averages with Buy Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

plt.gca().xaxis.set_major_locator(months)
plt.gca().xaxis.set_minor_locator(days)
plt.gca().xaxis.set_major_formatter(time_format)

# Subplot 2: Daily Returns 
plt.subplot(4, 1, 2)
colors = data['Daily_Return'].apply(lambda x: 'green' if x > 0 else 'red')
plt.bar(data.index, data['Daily_Return'], color=colors, alpha=0.6)
plt.title('Daily Returns')
plt.xlabel('Date')
plt.ylabel('Return')
plt.legend()

plt.gca().xaxis.set_major_locator(months)
plt.gca().xaxis.set_minor_locator(days)
plt.gca().xaxis.set_major_formatter(time_format)

# Subplot 3: Rolling Volatillity
plt.subplot(4, 1, 3)
plt.plot(data['Rolling_Volatility'], label='20-Day Rolling Volatility', color='indianred', alpha=0.75)
plt.title('20-Day Rolling Volatility')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()

plt.gca().xaxis.set_major_locator(months)
plt.gca().xaxis.set_minor_locator(days)
plt.gca().xaxis.set_major_formatter(time_format)

# Subplot 4: Relative Strength Index
plt.subplot(4, 1, 4)
plt.plot(data['RSI'], label='RSI', color='violet', alpha=0.75)
plt.axhline(70, color='red', linestyle='--') # Sell signals
plt.fill_between(data.index, data['RSI'], 70, where=(data['RSI'] >= 70), color='red', alpha=0.3)
plt.axhline(30, color='green', linestyle='--') # Buy signals
plt.fill_between(data.index, data['RSI'], 30, where=(data['RSI'] <= 30), color='green', alpha=0.3)
plt.title('Relative Strength Index (RSI)')
plt.xlabel('Date')
plt.ylabel('RSI')
plt.legend()

plt.gca().xaxis.set_major_locator(months)
plt.gca().xaxis.set_minor_locator(days)
plt.gca().xaxis.set_major_formatter(time_format)

plt.tight_layout()
plt.show()

