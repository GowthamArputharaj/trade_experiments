## SAMPLE RSI INDICATOR USING "ta" LIBRARY
# USE 'dir()' FUNCTION TO GET INBUILD FUNCTIONS AND DETAILS OF THE CLASS 

import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands

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


bb = BollingerBands(data['close'], 20, False)

print(bb)

print(dir(BollingerBands))

print(dir(bb))

# print(bb.bollinger_wband().head(40)) # IT GIVES THE RSI RESULT
# print(bb.bollinger_lband_indicator().head(40)) # IT GIVES THE RSI RESULT
print(bb.bollinger_mavg().head(40)) # IT GIVES THE RSI RESULT

exit()