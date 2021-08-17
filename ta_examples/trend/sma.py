## SAMPLE RSI INDICATOR USING "ta" LIBRARY
# USE 'dir()' FUNCTION TO GET INBUILD FUNCTIONS AND DETAILS OF THE CLASS 

import pandas as pd
from ta.utils import dropna
from ta.trend import SMAIndicator

# constant area
DATA_LENGTH = 500
START_DATA_LENGTH = 0
END_DATA_LENGTH = START_DATA_LENGTH + DATA_LENGTH

df = pd.read_csv("../../data/eurusd_col_m1_new.csv", sep=',')

df = df.iloc[START_DATA_LENGTH:END_DATA_LENGTH]

# df.Datetime = pd.to_datetime(df.Datetime)
# df = df.set_index('Datetime')

data = None

data = df.iloc[:DATA_LENGTH]


sma = SMAIndicator(data['close'], 14, False)

print(sma)

print(dir(SMAIndicator))

print(dir(sma))

print(sma.sma_indicator().head(20)) # IT GIVES THE Simple Moving Average RESULT

exit()