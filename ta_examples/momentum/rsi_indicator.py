## SAMPLE RSI INDICATOR USING "ta" LIBRARY
# USE 'dir()' FUNCTION TO GET INBUILD FUNCTIONS AND DETAILS OF THE CLASS 

import pandas as pd
from ta.utils import dropna
from ta.momentum import RSIIndicator

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


rsi = RSIIndicator(data['close'], 14, False)

print(rsi)

print(dir(RSIIndicator))

print(dir(rsi))
print(rsi.rsi().head(20)) # IT GIVES THE RSI RESULT

exit()