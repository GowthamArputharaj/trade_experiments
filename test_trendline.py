## SAMPLE RSI INDICATOR USING "ta" LIBRARY
# USE 'dir()' FUNCTION TO GET INBUILD FUNCTIONS AND DETAILS OF THE CLASS 

import pandas as pd
import pytrendline
import os

# constant area
DATA_LENGTH = 500
DATA_LENGTH = 100
# DATA_LENGTH = 40
START_DATA_LENGTH = 0
END_DATA_LENGTH = START_DATA_LENGTH + DATA_LENGTH

df = pd.read_csv("../data/eurusd_col_m1_new.csv", sep=',')

df = df.iloc[START_DATA_LENGTH:END_DATA_LENGTH]

df['Datetime'] = pd.to_datetime(df.Datetime)
df['Date'] = pd.to_datetime(df.Datetime)
# df = df.set_index('Datetime')
# df = df.set_index('Datetime')

# print(df)
# print(df['Datetime'])
# exit()

data = None

candles_df = df.iloc[:DATA_LENGTH]


# candlestick_data = pytrendline.CandlestickData(candles_df)


candlestick_data = pytrendline.CandlestickData(
  df=candles_df,
  # time_interval="1m", # choose between 1m,3m,5m,10m,15m,30m,1h,1d
  time_interval="5m", # choose between 1m,3m,5m,10m,15m,30m,1h,1d
  open_col="open", # name of the column containing candle "Open" price
  high_col="high", # name of the column containing candle "High" price
  low_col="low", # name of the column containing candle "Low" price
  close_col="close", # name of the column containing candle "Close" price
  datetime_col="Datetime" # name of the column containing candle datetime price (use none if datetime is in index)
)

print(candlestick_data)

results = pytrendline.detect(
  candlestick_data=candlestick_data,
)

print(results) # IT GIVES THE Simple Moving Average RESULT

outf = pytrendline.plot(
  results=results,
  filedir='.',
  filename='example_output.html',
)
# os.system("open " + outf)
os.system("start " + outf)

print('__END__')
exit()