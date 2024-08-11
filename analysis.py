import pandas as pd
import matplotlib.pyplot as plt

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

# Plot everything together
plt.figure(figsize=(14, 8))

# Subplot 1: Closing Price, Simple Moving Averages, and Buy Signals
plt.subplot(3, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue', alpha=0.3)
plt.plot(data['SMA_20'], label='20-Day SMA', color='red', alpha=0.6)
plt.plot(data['SMA_50'], label='50-Day SMA', color='green', alpha=0.6)
buy_signals = data[data['Buy_Signal']] # When price crosses above the 20-day SMA
plt.scatter(buy_signals.index, buy_signals['Close'], marker='o', color='green', s=50, label='Buy Signal', edgecolors='k')
plt.title('Stock Price and Moving Averages with Buy Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Subplot 2: Daily Returns 
plt.subplot(3, 1, 2)
plt.plot(data['Daily_Return'], label='Daily Returns', color='purple', alpha=0.6)
plt.title('Daily Returns')
plt.xlabel('Date')
plt.ylabel('Return')
plt.legend()

# Subplot 3: Rolling Volatillity
plt.subplot(3, 1, 3)
plt.plot(data['Rolling_Volatility'], label='20-Day Rolling Volatility', color='orange', alpha=0.75)
plt.title('Rolling Volatility')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()

plt.tight_layout()
plt.show()

