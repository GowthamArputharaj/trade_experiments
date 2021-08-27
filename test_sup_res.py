import trendln
import pandas as pd
import numpy as np
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
# from mplfinance import candlestick_ohlc
import mplfinance as mpf



# print(dir(trendln))
# print(dir(trendln.calc_support_resistance)

# exit()


trade_log = pd.read_csv('./data/eurusd_col_m1_new_caps.csv')

hist = trade_log

hist = hist.iloc[:500]

df = hist

def isSupport(df,i):
	support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
	return support

def isResistance(df,i):
	resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
	return resistance

levels = []
for i in range(2,df.shape[0]-2):
	if isSupport(df,i):
		levels.append((i,df['Low'][i]))
	elif isResistance(df,i):
		levels.append((i,df['High'][i]))

addplots = []


df.index = pd.DatetimeIndex(df['Datetime'])


def plot_all():
	fig, ax = plt.subplots()
	# one = mpf.make_addplot(pd.DataFrame(df['Close']), color='red')
	# print(one)
	# print(df['Close'])
	# exit()
	# addplots.append(one)
	# candlestick_ohlc(ax,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8)
	date_format = mpl_dates.DateFormatter('%d %b %Y')
	ax.xaxis.set_major_formatter(date_format)
	fig.autofmt_xdate()
	fig.tight_layout()

	for level in levels:
		a = np.empty([len(df.values)])
		a.fill(level[1])
		# print(level, a)
		# exit()
		addplots.append(mpf.make_addplot(pd.DataFrame(a),color='blue'))
		# addplots.append(mpf.make_addplot(pd.DataFrame(level[1]),panel=1,colors='blue'))
		# plt.hlines(level[1],xmin=df['Date'][level[0]], xmax=max(df['Date']),colors='blue')
		
	# print(a)
	# exit()
	# fig.show()
	pd.to_datetime(df.Datetime)
	mpf.plot(pd.DataFrame(df), addplot=addplots, type='candle', style="yahoo",figscale=1.2, volume=False)
	# mpf.plot(pd.DataFrame(df['Datetime'].to_datetime), addplot=addplots, type='candle', style="yahoo",figscale=1.2, volume=True)


s =  np.mean(df['High'] - df['Low'])

def isFarFromLevel(l):
	return np.sum([abs(l-x) < s  for x in levels]) == 0


levels = []
for i in range(2,df.shape[0]-2):
	if isSupport(df,i):
		l = df['Low'][i]
		if isFarFromLevel(l):
			levels.append((i,l))
	elif isResistance(df,i):
		l = df['High'][i]
		if isFarFromLevel(l):
			levels.append((i,l))


plot_all()



