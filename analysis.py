import pandas as pd
import matplotlib.pyplot as plt

# Import the data (replace the first parameter with any .csv stock data)
data = pd.read_csv('NVDA_stock_data.csv', index_col='Date', parse_dates=True)

# Calculate Simple Moving Averages
data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()

# Plot Closing Price, Moving Averages
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue', alpha=0.3)
plt.plot(data['SMA_20'], label='20-Day SMA', color='red', alpha=0.6)
plt.plot(data['SMA_50'], label='50-Day SMA', color='green', alpha=0.6)

plt.title('Stock Price and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()