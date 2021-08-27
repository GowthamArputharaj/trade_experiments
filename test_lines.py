# Get and Plot 
# all Trend lines, 
# Support and Resistance Lines, 
# Extreme Points 
# for given point or range of points

# Module Import Area
import pandas as pd 
import numpy as np 

import matplotlib.pyplot as plt 
import mplfinance as mpf

from datetime import datetime

from scipy.signal import argrelextrema
import time

import MetaTrader5 as mt5
import pytz

import colorama
from termcolor import colored, cprint

colorama.init()


trade_log = open("trade_log.txt", "a")

# Constants Area
## MetaTrader Credentials
MT_login = 67021181
# MT_password = "q14d6352C"
MT_password = "gR7wDjqx"
MT_server = "RoboForex-ECN"

symbol = 'EURUSD'
timeframe = mt5.TIMEFRAME_M1
# timeframe = mt5.TIMEFRAME_M2
# timeframe = mt5.TIMEFRAME_M3
# timeframe = mt5.TIMEFRAME_M5
# timeframe = mt5.TIMEFRAME_M15
# timeframe = mt5.TIMEFRAME_M30
# timeframe = mt5.TIMEFRAME_H1
# timeframe = mt5.TIMEFRAME_H4
# timeframe = mt5.TIMEFRAME_D1
# timeframe = mt5.TIMEFRAME_W1
# timeframe = mt5.TIMEFRAME_MN1

# symbols = ['EURUSD', 'AUDCAD', 'USDJPY', 'EURAUD']
# Low spread pairs
# symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF']
# symbols = ['EURUSD']
symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'EURJPY']
# symbols = ['EURUSD', 'GBPUSD']
# symbols = ['EURUSD', 'USDJPY', 'EURJPY', 'AUDCAD', 'EURAUD', 'GBPUSD']
# symbols = ['AUDNZD']
# symbols = ['EURUSD']

selected_symbol = 'EURUSD'

lot = 0.01

deviation = 20

magic = 12345678

TRADE_WITH_TREND = True

# [1, 5, 15, 30, 16385, 16388, 16408, 32769, 49153]
# [1, 5, 15, 30, 60, 240, 1440, 10080, 49153]

# last_candle_until_last_time = {
# 	'1_minute': 0,
# 	'5_minute': 0,
# 	'15_minute': 0,
# 	'30_minute': 0,
# 	'16385_minute': 0,
# 	'16388_minute': 0,
# 	'16408_minute': 0,
# 	'32769_minute': 0,
# 	'49153_minute': 0,
# }

last_candle_until_last_time = {
	'1_minute': {},
	'2_minute': {},
	'3_minute': {},
	'5_minute': {},
	'15_minute': {},
	'30_minute': {},
	'16385_minute': {},
	'16388_minute': {},
	'16408_minute': {},
	'32769_minute': {},
	'49153_minute': {},
}

no_of_seconds_for_timestamp_candle = {
	'1_minute': ( 60 * 1 ),
	'2_minute': ( 60 * 2 ),
	'3_minute': ( 60 * 3 ),
	'5_minute': ( 60 * 5 ),
	'15_minute': ( 60 * 15 ),
	'30_minute': ( 60 * 30 ),
	'16385_minute': ( 60 * 60 * 1 ),
	'16388_minute': ( 60 * 60 * 4 ),
	'16408_minute': ( 60 * 60 * 24 ),
	'32769_minute': ( 60 * 60 * 24 * 7 ),
	'49153_minute': 0,
}

stop_loss_take_profit = {
	'1_minute': {
		'stop_loss': 15,
		'trailing_stop_loss': 15,
		# 'trailing_stop_loss': 15,
	},
	'2_minute': {
		'stop_loss': 40,
		'trailing_stop_loss': 20,
	},
	'3_minute': {
		'stop_loss': 40,
		'trailing_stop_loss': 20,
	},
	'5_minute': {
		'stop_loss': 40,
		'trailing_stop_loss': 40,
	},
	'15_minute': {},
	'30_minute': {},
	'16385_minute': {},
	'16388_minute': {},
	'16408_minute': {},
	'32769_minute': {},
	'49153_minute': {},
}

mt_error_codes = {
	10004: 'Trade Retcode Requote ( Requote )',
	10006: 'Trade Retcode Reject ( Request Rejected )',
	10007: 'Trade Retcode Cancel ( Request Cancelled By Trader )',
	10008: 'Trade Retcode Placed ( Order Placed )',
	10009: 'Trade Retcode Done ( Request Placed )',
	10010: 'TRADE_RETCODE_DONE_PARTIAL ( Only part of the request was completed )',
	10011: 'TRADE_RETCODE_ERROR ( Request processing error)',
	10012: 'TRADE_RETCODE_TIMEOUT ( Request canceled by timeout)',
	10013: 'TRADE_RETCODE_INVALID ( Invalid request )',
	10014: 'TRADE_RETCODE_INVALID_VOLUME ( Invalid volume in the request )',
	10015: 'TRADE_RETCODE_INVALID_PRICE ( Invalid price in the request )',
	10016: 'TRADE_RETCODE_INVALID_STOPS ( Invalid stops in the request )',
	10017: 'TRADE_RETCODE_TRADE_DISABLED ( Trade is disabled )',
	10018: 'TRADE_RETCODE_MARKET_CLOSED ( Market is closed )',
	10019: 'TRADE_RETCODE_NO_MONEY ( There is not enough money to complete the request )',
	10020: 'TRADE_RETCODE_PRICE_CHANGED ( Prices changed )',
	10021: 'TRADE_RETCODE_PRICE_OFF ( There are no quotes to process the request )',
	10022: 'TRADE_RETCODE_INVALID_EXPIRATION ( Invalid order expiration date in the request )',
	10023: 'TRADE_RETCODE_ORDER_CHANGED ( Order state changed )',
	10024: 'TRADE_RETCODE_TOO_MANY_REQUESTS ( Too frequent requests )',
	10025: 'TRADE_RETCODE_NO_CHANGES ( No changes in request )',
	10026: 'TRADE_RETCODE_SERVER_DISABLES_AT ( Autotrading disabled by server )',
	10027: 'TRADE_RETCODE_CLIENT_DISABLES_AT ( Autotrading disabled by client terminal )',
	10028: 'TRADE_RETCODE_LOCKED ( Request locked for processing )',
	10029: 'TRADE_RETCODE_FROZEN ( Order or position frozen )',
	10030: 'TRADE_RETCODE_INVALID_FILL ( Invalid order filling type )',
	10031: 'TRADE_RETCODE_CONNECTION ( No connection with the trade server )',
	10032: 'TRADE_RETCODE_ONLY_REAL ( Operation is allowed only for live accounts )',
	10033: 'TRADE_RETCODE_LIMIT_ORDERS ( The number of pending orders has reached the limit )',
	10034: 'TRADE_RETCODE_LIMIT_VOLUME ( The volume of orders and positions for the symbol has reached the limit )',
	10035: 'TRADE_RETCODE_INVALID_ORDER ( Incorrect or prohibited order type )',
	10036: 'TRADE_RETCODE_POSITION_CLOSED ( Position with the specified POSITION_IDENTIFIER has already been closed )',
	10038: 'TRADE_RETCODE_INVALID_CLOSE_VOLUME ( A close volume exceeds the current position volume )',
	10039: 'TRADE_RETCODE_CLOSE_ORDER_EXIST ( check online for more ~ A close order already exists for a specified position. )',
	10040: 'TRADE_RETCODE_LIMIT_POSITIONS ( chec online for more ~ The number of open positions simultaneously present on an account can be limited by the server settings. )',
	10041: 'TRADE_RETCODE_REJECT_CANCEL ( The pending order activation request is rejected, the order is canceled )',
	10042: 'TRADE_RETCODE_LONG_ONLY ( The request is rejected, because the "Only long positions are allowed" rule is set for the symbol (POSITION_TYPE_BUY) )',
	10043: 'TRADE_RETCODE_SHORT_ONLY ( The request is rejected, because the "Only short positions are allowed" rule is set for the symbol (POSITION_TYPE_SELL) )',
	10044: 'TRADE_RETCODE_CLOSE_ONLY ( The request is rejected, because the "Only position closing is allowed" rule is set for the symbol )',
	10045: 'TRADE_RETCODE_FIFO_CLOSE ( The request is rejected, because "Position closing is allowed only by FIFO rule" flag is set for the trading account (ACCOUNT_FIFO_CLOSE=true) )',
	10046: 'TRADE_RETCODE_HEDGE_PROHIBITED ( The request is rejected, because the "Opposite positions on a single symbol are disabled" rule is set for the trading account. )',
}

# contains all live open positions in market
all_open_positions_from_market = pd.DataFrame()

# if hasTrailingStopLoss is True, the trailing stop loss position is updated
hasTrailingStopLoss = True 

PLOT_GRAPH_AFTER_OPEN_POSITION = False
# PLOT_GRAPH_AFTER_OPEN_POSITION = True

VOLATILITY_CHECK_VOLUME = float(0.0010)
VOLATILITY_CHECK_VOLUME_JPY = float(0.010)
MAXIMUM_CONSIDERABLE_DISTANCE_BETWEEN_LINE_AND_PRICE = float(0.0005)
NUMBER_OF_PIPS_BETWEEN_NEXT_LINE_AND_LAST_CANDLE_CLOSE_PRICE = 10

TREND_LINE_WEIGHT = 2
PITCHFORK_LINE_WEIGHT = 2
SUPPORT_RESISTANCE_WEIGHT = 2

# DontConsiderIsChartDataVolatile = False
DontConsiderIsChartDataVolatile = True
found_trend = None

## File Data Constants
CANDLE_DATA_FILE_NAME = "../../../data/eurusd_col_m1_new.csv"
READ_TOTAL_CSV_DATA = 500
EXTEND_LENGTH = 50
SCAN_LENGTH = 200
ROUND_DIGIT = 5
ROUND_CMP = 3
DATA_STARTING_POINT = 200
CDL_ROUND_DIGITS = 5
IGNORE_CANDLE_STATUS = False
MIN_SHAVEN_BODY = 1 * CDL_ROUND_DIGITS
MAX_STAR_BODY = 10 * (10 ** -CDL_ROUND_DIGITS)

## Extremes Constants
# EXTREMES_ORDER = 10
EXTREMES_ORDER = 6
EXTREME_POINTS_COLOR = 'red'
EXTREME_POINTS_INTERSECTION_COLOR = 'green'
MIN_MAX_EXTREME = ['extreme']

## Support Resistance Constants
SUPPORT_RESISTANCE_ROUND_CMP = 4
SUPPORT_RESISTANCE_LINE_COLOR = 'lime'
LINE_COLOR = 'blue'
LINES_AT_POINT_COLOR = 'purple'
NUMBER_OF_SUPPORT_RESISTANCE_LINES = 5
TOP_NUMBER_OF_SUPPORT_AND_RESISTANCE_OCCURANCE = 50000000

## Pitchfork Constants
# PITCHFORK_EXTREMES_RANGES = [10]
PITCHFORK_EXTREMES_RANGES = [6]
NUMBER_OF_PITCHFORK_PER_RANGE = 1
PITCHFORK_EXTEND_LENGTH = 40
PITCHFORK_MINIMUM_BC_HEIGHT = 0.00005
#.. first_point to second_point distance can be (PITCHFORK_TAIL_TO_FORK_WIDTH) times distance between second_point to third_point
PITCHFORK_TAIL_TO_FORK_WIDTH = 2 
MAX_EXTREME_POINT_GAP_FOR_ONE_PITCHFORK = 3
# MAX_EXTREMES_FOR_SECOND_PITCHFORK = 2
# MAX_EXTREMES_FOR_THIRD_PITCHFORK = 3
MAX_EXTREMES_FOR_SECOND_PITCHFORK = 3
MAX_EXTREMES_FOR_THIRD_PITCHFORK = 3

# Oscillators
WILLIAM_R_COLOR = 'blue'
RSI_COLOR = 'green'

# 7.500000000004725e-05
# 0.00007500000000004725

# Arrays Area
## Lines Arrays
all_lines = []
all_lines_for_extreme_points = []
all_support_and_resistance_lines = []
all_line_points_at_point = []
all_support_resistance_lines = []
all_sup_res_line_points_at_point = []
all_pitchfork_line_points_at_point = []

## Extremes Arrays
all_points = []
all_minimas = []
all_maximas = []
all_extremes = []

## Pitchfork Arrays
all_minimas_pitchfork = []
all_maximas_pitchfork = []
all_extremes_pitchfork = []
all_extreme_pitchfork_points = []
all_pitchfork_points = []
all_upward_pitchfork_points = []
all_downward_pitchfork_points = []
all_pitchfork_lines = []

## Graph Arrays
selectPlotCandleStickGraph = []

## Oscillators
william_r_oscillator = []
stochastic_oscillator = []
rsi_oscillator = []
obv_oscillator = []

## CandleSticks 
all_candlestick_patterns = []
all_candlestick_predictions = []

## Trade 
all_last_candle_patterns = {}
future_close_positions = []
future_close_positions_log = []

# Initial something
data = []
function_initial_data = []


global_variables_to_reset = ['function_initial_data', 'data', 'all_candlestick_patterns', 'all_candlestick_predictions', 'william_r_oscillator', 'stochastic_oscillator', 'rsi_oscillator', 'obv_oscillator', 
'all_minimas_pitchfork', 'all_maximas_pitchfork', 'all_extremes_pitchfork', 'all_extreme_pitchfork_points',
'all_pitchfork_points', 'all_upward_pitchfork_points', 'all_downward_pitchfork_points', 'all_pitchfork_lines',
'selectPlotCandleStickGraph', 'all_lines', 'all_lines_for_extreme_points', 'all_support_and_resistance_lines',
'all_line_points_at_point', 'all_support_resistance_lines', 'all_sup_res_line_points_at_point', 'all_pitchfork_line_points_at_point',
'all_points', 'all_minimas', 'all_maximas', 'all_extremes', ]


def initializeMetaTrader():
	if not mt5.initialize(login=MT_login, server=MT_server,password=MT_password):
		print("initialize() failed, error code =",mt5.last_error())
		quit()
	
	cprint("MetaTrader5 package author: " + str(mt5.__author__), 'white', 'on_blue')
	cprint("MetaTrader5 package version: " + str(mt5.__version__), 'white', 'on_blue')

def getChartData():
	global data, function_initial_data
	# establish connection to MetaTrader 5 terminal
	# if not mt5.initialize():

	# symbol = "USDJPY"
	# symbol = "EURUSD"
	# timeframe = mt5.TIMEFRAME_M15
	# timeframe = mt5.TIMEFRAME_M30
	# timeframe = mt5.TIMEFRAME_M5

	# set time zone to UTC
	# timezone = pytz.timezone("Etc/UTC")
	timezone = pytz.timezone("Etc/GMT-3") # toggles according to season (NYSE) ( summer, winter )
	# timezone = pytz.timezone("Etc/GMT-2") # toggles according to season (NYSE) ( summer, winter )


	# create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
	now = datetime.now(timezone)
	timestamp = datetime.timestamp(now)
	timestamp = int(timestamp)

	current_year = int(now.strftime("%Y"))
	current_month = int(now.strftime("%m"))
	current_date = int(now.strftime("%d"))
	current_hour = int(now.strftime("%H"))
	current_minute = int(now.strftime("%M"))
	current_second = int(now.strftime("%S"))

	# for i in range(120):
	# 	now = datetime.now(timezone)
	# 	current_second = int(now.strftime("%S"))
	# 	print(current_second)
	# 	time.sleep(1)
	# exit()

	# print(current_year, current_month, current_date, current_hour, current_minute )

	from_month = current_month 
	from_year = current_year 
	from_date = current_date 


	if(timeframe == mt5.TIMEFRAME_M1):
		last_candle_until_last_time['1_minute'][selected_symbol] = timestamp
		from_month = current_month - 1
	if(timeframe == mt5.TIMEFRAME_M2):
		last_candle_until_last_time['2_minute'][selected_symbol] = timestamp
		from_month = current_month - 1
	if(timeframe == mt5.TIMEFRAME_M3):
		last_candle_until_last_time['3_minute'][selected_symbol] = timestamp
		from_month = current_month - 1
	if(timeframe == mt5.TIMEFRAME_M5):
		last_candle_until_last_time['5_minute'][selected_symbol] = timestamp
		from_month = current_month - 1
	if(timeframe == mt5.TIMEFRAME_M15):
		last_candle_until_last_time['15_minute'][selected_symbol] = timestamp
		from_month = current_month - 2
		from_date = 15
	if(timeframe == mt5.TIMEFRAME_M30):
		last_candle_until_last_time['30_minute'][selected_symbol] = timestamp
		from_month = current_month - 2
	if(timeframe == mt5.TIMEFRAME_H1):
		last_candle_until_last_time['16385_minute'][selected_symbol] = timestamp
		from_month = current_month - 2
	if(timeframe == mt5.TIMEFRAME_H4):
		last_candle_until_last_time['16388_minute'][selected_symbol] = timestamp
		from_month = current_month - 2
	if(timeframe == mt5.TIMEFRAME_D1):
		last_candle_until_last_time['16408_minute'][selected_symbol] = timestamp
		from_month = 1
		from_year = current_year - 1
	if(timeframe == mt5.TIMEFRAME_W1):
		last_candle_until_last_time['32769_minute'][selected_symbol] = timestamp
		from_month = 1
		from_year = current_year - 5
	if(timeframe == mt5.TIMEFRAME_MN1):
		last_candle_until_last_time['49153_minute'] = timestamp
		from_month = current_month
		from_year = current_year - 25

	if(current_date == 30):
		current_month = current_month + 1
		current_date = 1

	utc_from = datetime(from_year, from_month, from_date, tzinfo=timezone)
	utc_to = datetime(current_year, current_month, current_date+2, tzinfo=timezone)
	# utc_to = datetime(current_year, current_month, current_date, hour = 6, minute = 10, tzinfo=timezone)
	# utc_to = datetime(2020, 1, 11, hour = 13, tzinfo=timezone)
	# get bars from USDJPY M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
	# rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, utc_from, utc_to)
	rates = mt5.copy_rates_range(selected_symbol, timeframe, utc_from, utc_to)
	# rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_D1, utc_from, utc_to)
	# rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, utc_from, utc_to)

	# shut down connection to the MetaTrader 5 terminal
	# mt5.shutdown()

	# create DataFrame out of the obtained data
	rates_frame = pd.DataFrame(rates)
	# print(rates_frame, symbol, timeframe, utc_from, utc_to)
	# exit()

	# print(rates_frame)

	rates_frame['Datetime']=pd.to_datetime(rates_frame['time'], unit='s')
	# rates_frame['Timestamp']=rates_frame['time']

	data = rates_frame[['Datetime', 'open', 'high', 'low', 'close', 'tick_volume']]

	data.columns = ['Datetime', 'open', 'high', 'low', 'close', 'volume']

	# data = data.iloc[:READ_TOTAL_CSV_DATA]
	data = data.tail(READ_TOTAL_CSV_DATA)
	data.Datetime = pd.to_datetime(data.Datetime)
	data = data.set_index('Datetime')

	temp = data.copy()
	temp = pd.DataFrame(temp)
	temp = temp.iloc[:-1]

	function_initial_data = pd.DataFrame(temp).tail(SCAN_LENGTH+EXTEND_LENGTH)
	# df = pd.DataFrame(df)
	# print(function_initial_data.tail(5))
	# print(function_initial_data.head(5))
	# print(function_initial_data.iloc[len(df)-1])
	# exit()

def getAllBullishBearishChangingPoints(returnOpenCloseData = False, returnLowHighData = False):
	# dtt = function_initial_data.iloc[:]
	dtt = function_initial_data.iloc[DATA_STARTING_POINT:DATA_STARTING_POINT+SCAN_LENGTH]
	points = []
	low_high_data = []
	open_close_data = []

	for i in range(len(dtt)-1):
		i_stat = isPointBullishOrBearish(i)
		i_plus_one_stat = isPointBullishOrBearish(i+1)

		if(i_stat != i_plus_one_stat):
			if((returnOpenCloseData == False) and (returnLowHighData == False)):
				points.append(dtt.iloc[i+1])
		
			if(returnOpenCloseData == True):
				if(i_stat == 'Bullish' and i_plus_one_stat == 'Bearish'):
					open_close_data.append(dtt['close'].iloc[i+1])
				if(i_stat == 'Bearish' and i_plus_one_stat == 'Bullish'):
					open_close_data.append(dtt['open'].iloc[i+1])
			
			if(returnLowHighData == True):
				if(i_stat == 'Bullish' and i_plus_one_stat == 'Bearish'):
					low_high_data.append(dtt['high'].iloc[i+1])
				if(i_stat == 'Bearish' and i_plus_one_stat == 'Bullish'):
					low_high_data.append(dtt['low'].iloc[i+1])
			
	if((returnOpenCloseData == False) and (returnLowHighData == False)):
		return points
	else:
		return open_close_data, low_high_data

def isPointBullishOrBearish(x_point):
	point = function_initial_data.iloc[x_point]
	result = ''
	if(point['close'] < point['open']):
		result = 'Bearish'
	elif(point['open'] < point['close']):
		result = 'Bullish'
	else:
		result = 'Doji'
	
	return result 

def isPointValueBullishOrBearish(point):
	result = ''
	if(point['close'] < point['open']):
		result = 'Bearish'
	elif(point['open'] < point['close']):
		result = 'Bullish'
	else:
		result = 'Doji'
	
	return result 

def pointExtremeInOpenOrClose(x_point, global_variable = []):
	global all_minimas_pitchfork
	
	result = 'close'
	isPointBullishOrBearishResult = isPointBullishOrBearish(x_point)

	if(len(global_variable) == 0):
		if(isPointBullishOrBearishResult == 'Doji'):
			result = 'open'

		if(x_point in all_minimas):
			result = 'open' if(isPointBullishOrBearishResult == 'Bullish') else 'close'

		if(x_point in all_maximas):
			result = 'close' if(isPointBullishOrBearishResult == 'Bullish') else 'open'

	elif('pitchfork' in global_variable):
		if(isPointBullishOrBearishResult == 'Doji'):
			result = 'open'

		if(x_point in all_minimas_pitchfork):
			result = 'open' if(isPointBullishOrBearishResult == 'Bullish') else 'close'

		if(x_point in all_maximas_pitchfork):
			result = 'close' if(isPointBullishOrBearishResult == 'Bullish') else 'open'

	return result

def getMinimaPoints(order = EXTREMES_ORDER, set_global_variable = True): 
	global all_minimas
	global all_minimas_pitchfork

	data = file_data = []
	if(set_global_variable == 'pitchfork'):
		file_data = function_initial_data.iloc[:SCAN_LENGTH]
	else:
		file_data = function_initial_data.iloc[:SCAN_LENGTH]

	for i in range(len(file_data)):
		point = file_data.iloc[i]

		isPointValueBullishOrBearishResult = isPointValueBullishOrBearish(point)
		if(isPointValueBullishOrBearishResult == 'Bullish'):
			data.append(point['open'])
		elif(isPointValueBullishOrBearishResult == 'Bearish'):
			data.append(point['close'])
		else:
			data.append(point['open'])

	min_idx = list(argrelextrema(np.array(data), np.less, order=order)[0])
	
	if(set_global_variable == True):
		all_minimas = min_idx
	elif(set_global_variable == 'pitchfork'):
		all_minimas_pitchfork = min_idx

	return min_idx

def getMaximaPoints(order = EXTREMES_ORDER, set_global_variable = True):
	global all_maximas
	global all_maximas_pitchfork

	data = file_data = []
	if(set_global_variable == 'pitchfork'):
		file_data = function_initial_data.iloc[:SCAN_LENGTH]
	else:
		file_data = function_initial_data.iloc[:SCAN_LENGTH]

	for i in range(len(file_data)):
		point = file_data.iloc[i]
		
		isPointValueBullishOrBearishResult = isPointValueBullishOrBearish(point)
		if(isPointValueBullishOrBearishResult == 'Bullish'):
			data.append(point['close'])
		elif(isPointValueBullishOrBearishResult == 'Bearish'):
			data.append(point['open'])
		else:
			data.append(point['close'])

	max_idx = list(argrelextrema(np.array(data), np.greater, order=order)[0])
	if(set_global_variable == True):
		all_maximas = max_idx
	elif(set_global_variable == 'pitchfork'):
		all_maximas_pitchfork = max_idx

	return max_idx

def getExtremePoints(sort = False, order = EXTREMES_ORDER, set_global_variable = True):
	global all_extremes
	global all_extremes_pitchfork

	if(set_global_variable == True):
		min_points = getMinimaPoints(order)
		max_points = getMaximaPoints(order)
		extreme_points = min_points + max_points

		if(sort == True):
			extreme_points.sort()

		all_extremes = extreme_points

	elif(set_global_variable == 'pitchfork'):
		min_points = getMinimaPoints(order, 'pitchfork')
		max_points = getMaximaPoints(order, 'pitchfork')
		extreme_points = min_points + max_points

		if(sort == True):
			extreme_points.sort()

		all_extremes_pitchfork = extreme_points
		
	return extreme_points

def getTwoPoints(first_point, second_point, length):
	points = [None] * length 
	points[first_point] = function_initial_data.iloc[first_point]
	points[second_point] = function_initial_data.iloc[second_point]
	return points

def getAllPoints(set_global_variable=[], length = SCAN_LENGTH+EXTEND_LENGTH, extremes = []): # max of extremas < length
	global all_points
	global all_extremes_pitchfork
	global all_extreme_pitchfork_points

	all_points = []
	points = [None] * length 

	# if(len(extremes) > 0):
	# 	if(max(extremes) < length):
	# 		raise Exception("Hi Gowtham!!! 'Maximum value of Extremas' should be greater then 'length'")

	if(len(extremes) == 0):
		if(len(set_global_variable) == 0):
			if('min' in MIN_MAX_EXTREME):
				[extremes.append(k) for k in all_minimas]
			if('max' in MIN_MAX_EXTREME ):
				[extremes.append(k) for k in all_maximas]
			if('extreme' in MIN_MAX_EXTREME):
				[extremes.append(k) for k in all_extremes]
		if('pitchfork' in set_global_variable):
			extremes = all_extremes_pitchfork
		

	for extreme_point in extremes:
		if(extreme_point < length):
			pointInOpenOrCloseResult = pointExtremeInOpenOrClose(extreme_point)

			if(pointInOpenOrCloseResult == 'close'):
				points[extreme_point] = function_initial_data['close'].iloc[extreme_point]
	
			if(pointInOpenOrCloseResult == 'open'):
				points[extreme_point] = function_initial_data['open'].iloc[extreme_point]

	if(len(set_global_variable) == 0):
		all_points = points 
	if('pitchfork' in set_global_variable):
		all_extreme_pitchfork_points = points 

	return points

def getOneLine(x1, y1, x2, y2, starting_point = 0, ending_point = SCAN_LENGTH + EXTEND_LENGTH):

	# slope
	m = (y2 - y1) / (x2 - x1)

	# intercept
	b = y1 - (m * x1)

	line_length = SCAN_LENGTH + EXTEND_LENGTH
	line = [None] * line_length

	for i in range(line_length):
		if(i >= starting_point and i < ending_point):
			line[i] = (m * i) + b

	return line

def getAllLinesForExtremePoints(extremes = []):
	global all_lines_for_extreme_points
	all_lines_for_extreme_points = []
	lines = []
	if(len(extremes) == 0):
		if('min' in MIN_MAX_EXTREME):
			[extremes.append(k) for k in all_minimas]
		if('max' in MIN_MAX_EXTREME ):
			[extremes.append(k) for k in all_maximas]
		if('extreme' in MIN_MAX_EXTREME):
			[extremes.append(k) for k in all_extremes]

	for i in range(len(extremes)-1):
		x1 = extremes[i]
		stat = pointExtremeInOpenOrClose(x1)
		y1 = function_initial_data[stat].iloc[x1]
		x2 = extremes[i+1]
		stat = pointExtremeInOpenOrClose(x2)
		y2 = function_initial_data[stat].iloc[x2]

		line = getOneLine(x1, y1, x2, y2)

		lines.append(line)

	all_lines_for_extreme_points = lines
	return all_lines_for_extreme_points

def getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = 0, ending_point = SCAN_LENGTH + EXTEND_LENGTH):
	# find line slope
	m = (y2 - y1) / (x2 - x1)

	# find parallel line equation 
	# y = mx + b 
	b = yy - ( m * xx )

	line_length = SCAN_LENGTH + EXTEND_LENGTH
	line = [None] * line_length

	for i in range(line_length):
		if(i >= starting_point and i < ending_point):
			line[i] = (m * i) + b

	return line

def getLinePointsAtPoint(x_value):
	global all_line_points_at_point
	
	points = []
	for line in all_lines_for_extreme_points:
		if(x_value < len(line)):
			pt = line[x_value]
			points.append(pt)
	
	all_line_points_at_point = points
	return points

def getSupportAndResistanceLines():
	global all_support_and_resistance_lines
	lines = []
	points = []

	points_open_close_data, points_low_close_data = getAllBullishBearishChangingPoints(returnOpenCloseData = True, returnLowHighData = True)
	[points.append(round(point, SUPPORT_RESISTANCE_ROUND_CMP)) for point in points_open_close_data]
	[points.append(round(point, SUPPORT_RESISTANCE_ROUND_CMP)) for point in points_low_close_data]
	
	unique_points, points_count = np.unique(points, return_counts = True)

	points_count = np.unique(points_count)
	points_count.sort()
	points_count = points_count[-TOP_NUMBER_OF_SUPPORT_AND_RESISTANCE_OCCURANCE:] # gets last 5 i.e top 5 biggest nos
	points_count = list(points_count) # [5, 3, 9, 7]
	points_count.reverse() # [9, 7, 5, 3] giving more priority to more occured point
	
	# NUMBER_OF_SUPPORT_RESISTANCE_LINES = 3
	no_of_sup_res_lines_found = 0
	for point_count in points_count:
		if((no_of_sup_res_lines_found < NUMBER_OF_SUPPORT_RESISTANCE_LINES) and (point_count > 5)):
			for unique_pt in unique_points:
				unique_point_count = points.count(unique_pt)
				if(unique_point_count == point_count):
					line = [unique_pt] * (SCAN_LENGTH + EXTEND_LENGTH)
					lines.append(line)
					no_of_sup_res_lines_found = no_of_sup_res_lines_found + 1
					if(no_of_sup_res_lines_found == NUMBER_OF_SUPPORT_RESISTANCE_LINES):
						break
		else:
			break
	
	all_support_and_resistance_lines = lines
	return all_support_and_resistance_lines

def getSupportResistanceLinePointsAtPoint(x_value):
	global all_sup_res_line_points_at_point
	
	points = []
	for line in all_support_and_resistance_lines:
		if(x_value < len(line)):
			pt = line[x_value]
			points.append(pt)
	
	all_sup_res_line_points_at_point = points
	return points

def getPitchforkPoints(): 
	global all_pitchfork_points
	ranges = PITCHFORK_EXTREMES_RANGES
	drawing_length = len(function_initial_data) - EXTEND_LENGTH

	merged_all_extremes_pitchfork = []

	for range_i in ranges:
		getMinimaPoints(range_i, set_global_variable = 'pitchfork')
		getMaximaPoints(range_i, set_global_variable = 'pitchfork')
		getExtremePoints(sort = True, order = range_i, set_global_variable = 'pitchfork')
		merged_all_extremes_pitchfork.extend(all_extremes_pitchfork)

	merged_all_extremes_pitchfork = list(np.unique(merged_all_extremes_pitchfork))

	ranges = list(np.unique(ranges))

	for range_i in ranges:
		desc_all_extremes_pitchfork = merged_all_extremes_pitchfork
		desc_all_extremes_pitchfork.reverse()

		no_of_pitchforks_found_per_range = 0
		check_upward_pitchfork = True 
		check_downward_pitchfork = True

		if(no_of_pitchforks_found_per_range < NUMBER_OF_PITCHFORK_PER_RANGE):
			for i in range(len(desc_all_extremes_pitchfork)):
				# Upward Pitchfork min-max-min point
				if(check_upward_pitchfork == True): 
					if(desc_all_extremes_pitchfork[i] in all_minimas_pitchfork): # if point is minima
						temp_extremes = desc_all_extremes_pitchfork[i:]
						jj = 1
						for j in range(i, len(desc_all_extremes_pitchfork)):
							jj = jj + 1
							if(desc_all_extremes_pitchfork[j] in all_maximas_pitchfork): # if point is maxima
								temp_extremes = desc_all_extremes_pitchfork[j:]
								kk = 1
								for k in range(j, len(desc_all_extremes_pitchfork)):
									kk = kk + 1
									if(desc_all_extremes_pitchfork[k] in all_minimas_pitchfork): # if point is minima
										first_point = desc_all_extremes_pitchfork[k]
										second_point = desc_all_extremes_pitchfork[j]
										third_point = desc_all_extremes_pitchfork[i]
										
										stat = pointExtremeInOpenOrClose(second_point, 'pitchfork')
										second_point_y = function_initial_data[stat].iloc[second_point]
										stat = pointExtremeInOpenOrClose(third_point, 'pitchfork')
										third_point_y = function_initial_data[stat].iloc[third_point]

										if(second_point_y > third_point_y):
											temp = [first_point, second_point, third_point]
											temp = np.unique(temp)
											if(len(temp) == 3):
												temp = list(temp)
												temp.append('UPWARD')
												all_pitchfork_points.append(temp)
												all_upward_pitchfork_points.append(temp)

									if(kk > MAX_EXTREMES_FOR_SECOND_PITCHFORK):
										break
										print('')
										print(desc_all_extremes_pitchfork[k], desc_all_extremes_pitchfork[j], desc_all_extremes_pitchfork[i])

							if(jj > MAX_EXTREMES_FOR_THIRD_PITCHFORK):
								break
								print('')


				# Downward Pitchfork min-max-min point
				if(check_downward_pitchfork == True):
					if(desc_all_extremes_pitchfork[i] in all_maximas_pitchfork): # if point is maxima
						temp_extremes = desc_all_extremes_pitchfork[i:]
						jj = 1
						for j in range(i, len(desc_all_extremes_pitchfork)):
							jj = jj + 1
							if(desc_all_extremes_pitchfork[j] in all_minimas_pitchfork): # if point is minima
								temp_extremes = desc_all_extremes_pitchfork[j:]
								kk = 1
								for k in range(j, len(desc_all_extremes_pitchfork)): 
									kk = kk + 1
									if(desc_all_extremes_pitchfork[k] in all_maximas_pitchfork): # if point is maxima
										first_point = desc_all_extremes_pitchfork[k]
										second_point = desc_all_extremes_pitchfork[j]
										third_point = desc_all_extremes_pitchfork[i]
										
										stat = pointExtremeInOpenOrClose(second_point, 'pitchfork')
										second_point_y = function_initial_data[stat].iloc[second_point]
										stat = pointExtremeInOpenOrClose(third_point, 'pitchfork')
										third_point_y = function_initial_data[stat].iloc[third_point]

										if(second_point_y < third_point_y):
											temp = [first_point, second_point, third_point]
											temp = np.unique(temp)
											if(len(temp) == 3):
												temp = list(temp)
												temp.append('DOWNWARD')
												all_pitchfork_points.append(temp)
												all_downward_pitchfork_points.append(temp)
				
									if(kk > MAX_EXTREMES_FOR_SECOND_PITCHFORK):
										break
										print('')
										print(desc_all_extremes_pitchfork[k], desc_all_extremes_pitchfork[j], desc_all_extremes_pitchfork[i])

		
							if(jj > MAX_EXTREMES_FOR_THIRD_PITCHFORK):
								break
								print('')

		else:
			# continue
			# break
			print('No of Pitchfork has reached to Maximum ')


	temp = all_pitchfork_points
	temp.sort()
	temp = np.unique(temp, axis=0)
	all_pitchfork_points = temp
	# all_pitchfork_points.append(temp)
	# temp = np.unique(all_pitchfork_points, axis=0)
	# all_pitchfork_points = temp

def getPitchforkLines(withTypes = ['andrew']): # regular_schiff, modified_schiff, andrew,
	global all_pitchfork_points, all_pitchfork_lines

	# sets all_minimas, all_maximas
	getExtremePoints()
	
	for pitchfork_points in all_pitchfork_points:

		pitchfork_line = []

		first_point = int(pitchfork_points[0])
		second_point = int(pitchfork_points[1])
		third_point = int(pitchfork_points[2])

		# line BC
		x1 = second_point
		stat_y1 = pointExtremeInOpenOrClose(x1, 'pitchfork')
		
		if(stat_y1 == None):
			raise Exception("Hi Gowtham!!! Pitchfork: Point is not within Extreme Point getPitchforkLines() ")
			
		y1 = function_initial_data[stat_y1].iloc[x1]

		x2 = third_point
		stat_y2 = pointExtremeInOpenOrClose(x2, 'pitchfork')
		y2 = function_initial_data[stat_y2].iloc[x2]

		line_BC = getOneLine(x1, y1, x2, y2, starting_point = x1, ending_point = x2+1)

		# midpoint of line BC ( D )
		mid_x = (x1 + x2) / 2
		mid_x = int(mid_x)
		mid_y = (y1 + y2) / 2

		# line AD
		x1 = first_point
		stat_y1 = pointExtremeInOpenOrClose(x1, 'pitchfork')
		
		if(stat_y1 == ''):
			raise Exception("Hi Gowtham!!! Pitchfork: Point is not within Extreme Point getPitchforkLines() ")

		y1 = function_initial_data[stat_y1].iloc[x1]

		x2 = mid_x
		y2 = mid_y

		pitchfork_starting_point = x1

		if((x2 + PITCHFORK_EXTEND_LENGTH) < (SCAN_LENGTH + EXTEND_LENGTH)):
			pitchfork_ending_point = x2 + PITCHFORK_EXTEND_LENGTH
		else: 
			pitchfork_ending_point = SCAN_LENGTH + EXTEND_LENGTH

		if(abs(y1 - y2) < PITCHFORK_MINIMUM_BC_HEIGHT):
			# helow there
			continue

		# line_AD = getOneLine(x1, y1, x2, y2, starting_point = pitchfork_starting_point, ending_point = pitchfork_ending_point)
		line_AD = getOneLine(x1, y1, x2, y2, starting_point = pitchfork_starting_point)

		# check BC to AD(to midpoint) ratio

		a_mid = abs(first_point - second_point)
		b_c = abs(second_point - third_point)

		if((a_mid/PITCHFORK_TAIL_TO_FORK_WIDTH) > b_c):
			continue


		# Parallel lines 
		# x1, y1, x2, y2 are from AD point ( since it is parallel line )

		# Parallel line from second point 
		xx = second_point 
		stat_y1 = pointExtremeInOpenOrClose(xx, 'pitchfork')
		yy = function_initial_data[stat_y1].iloc[xx]

		starting_point = xx

		# second_parallel_line = getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = starting_point, ending_point = pitchfork_ending_point)
		second_parallel_line = getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = starting_point)
		
		# parallel line from third point
		xx = third_point 
		stat_y1 = pointExtremeInOpenOrClose(xx, 'pitchfork')
		yy = function_initial_data[stat_y1].iloc[xx]

		starting_point = xx

		# third_parallel_line = getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = starting_point, ending_point = pitchfork_ending_point)
		third_parallel_line = getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = starting_point)

		# plt.plot(range(len(line_BC)), line_BC)
		# plt.plot(range(len(line_AD)), line_AD)
		# plt.plot(range(len(second_parallel_line)), second_parallel_line)
		# plt.plot(range(len(third_parallel_line)), third_parallel_line)

		# plt.show()
		# exit()

		line_AD_none_count = line_AD.count(None)
		line_BC_none_count = line_BC.count(None)
		second_parallel_none_count = second_parallel_line.count(None)
		third_parallel_none_count = third_parallel_line.count(None)

		if((line_AD_none_count < len(line_AD)) and 
		(line_BC_none_count < len(line_BC)) and 
		(second_parallel_none_count < len(second_parallel_line)) and 
		(third_parallel_none_count < len(third_parallel_line))):
	
			pitchfork_lines = [line_AD, line_BC, second_parallel_line, third_parallel_line]

			all_pitchfork_lines.append(pitchfork_lines)

def getPitchforkLinePointsAtPoint(x_value):
	global all_pitchfork_line_points_at_point
	
	points = []
	for pitchfork in all_pitchfork_lines:
		for line in pitchfork:
			if(x_value < len(line)):
				pt = line[x_value]
				points.append(pt)
	
	all_pitchfork_line_points_at_point = points
	return points

def plotCandleStickGraph(selectGraph):
	addplots = []
	
	if(('lines' in selectGraph) == True):	
		for line in all_lines_for_extreme_points:
			line_plot = mpf.make_addplot(pd.DataFrame(line, dtype="float"), type="line", color=LINE_COLOR)
			addplots.append(line_plot)

	if(('points' in selectGraph) == True):
		point_plot = mpf.make_addplot(pd.DataFrame(all_points, dtype="float"), type="scatter", color=EXTREME_POINTS_COLOR)
		addplots.append(point_plot)

	if(('line_points' in selectGraph) == True):
		length = SCAN_LENGTH + EXTEND_LENGTH
		points = []
		for i in all_line_points_at_point:
			pt = [None] * length
			pt[SCAN_LENGTH] = i
			point = mpf.make_addplot(pd.DataFrame(pt, dtype="float"), type="scatter", color=LINES_AT_POINT_COLOR)
			addplots.append(point)
	
	if(('support_resistance' in selectGraph) == True):
		color_i = 0
		for line in all_support_and_resistance_lines:
			line_plot = mpf.make_addplot(pd.DataFrame(line, dtype="float"), type="line", color=SUPPORT_RESISTANCE_LINE_COLOR)
			# line_plot = mpf.make_addplot(pd.DataFrame(line, dtype="float"), type="line", color=(250/1000, (125+color_i)/1000, 0))
			addplots.append(line_plot)
			color_i = color_i + 50

	if(('pitchfork' in selectGraph) == True):
		pitchfork_colors = ['red', 'blue', 'darkorange', 'purple', 'darkslategrey', 'darkgreen', 'darkviolet', 'orange', 'steelblue']
		for i in range(len(all_pitchfork_lines)):
			if(i > 0):
				color_index = i % len(pitchfork_colors)
				pitchfork_color = pitchfork_colors[color_index]

				for idx, pitchfork_line in enumerate(all_pitchfork_lines[i]):
					line_plot = mpf.make_addplot(pd.DataFrame(pitchfork_line, dtype="float"), type="line", color=pitchfork_color)
					addplots.append(line_plot)
			
	if(('william_r' in selectGraph) == True):
		# for point in william_r_oscillator:
		line_plot = mpf.make_addplot(pd.DataFrame(william_r_oscillator, dtype="float"),panel=1, color=WILLIAM_R_COLOR)
		addplots.append(line_plot)
			
	if(('stochastic' in selectGraph) == True):
		# for point in william_r_oscillator:
		line_plot = mpf.make_addplot(pd.DataFrame(stochastic_oscillator, dtype="float"),panel=1, color=WILLIAM_R_COLOR)
		addplots.append(line_plot)
			
	if(('rsi' in selectGraph) == True):
		# for point in william_r_oscillator:
		line_plot = mpf.make_addplot(pd.DataFrame(rsi_oscillator, dtype="float"),panel=1, color=RSI_COLOR)
		addplots.append(line_plot)
			
	if(('obv' in selectGraph) == True):
		# for point in obv_oscillator:
		line_plot = mpf.make_addplot(pd.DataFrame(obv_oscillator, dtype="float"),panel=1, color=RSI_COLOR)
		addplots.append(line_plot)
			
	if(('rsi' in selectGraph) or ('william_r' in selectGraph) or ('stochastic' in selectGraph) or ('obv' in selectGraph)):
		oscillator_line_eight = [None] * (SCAN_LENGTH+EXTEND_LENGTH)
		oscillator_line_seven = [None] * (SCAN_LENGTH+EXTEND_LENGTH)
		oscillator_line_three = [None] * (SCAN_LENGTH+EXTEND_LENGTH)
		oscillator_line_two = [None] * (SCAN_LENGTH+EXTEND_LENGTH)

		for i in range(SCAN_LENGTH+EXTEND_LENGTH):
			ones_digit = i % 10
			if(ones_digit in [1, 2, 3, 4, 5]):
				oscillator_line_eight[i] = 0.8	
				oscillator_line_seven[i] = 0.7
				oscillator_line_three[i] = 0.3
				oscillator_line_two[i] = 0.2

		line_plot = mpf.make_addplot(pd.DataFrame(oscillator_line_eight, dtype="float"),panel=1, color='red')
		addplots.append(line_plot)
		line_plot = mpf.make_addplot(pd.DataFrame(oscillator_line_seven, dtype="float"),panel=1, color='red')
		addplots.append(line_plot)
		line_plot = mpf.make_addplot(pd.DataFrame(oscillator_line_three, dtype="float"),panel=1, color='red')
		addplots.append(line_plot)
		line_plot = mpf.make_addplot(pd.DataFrame(oscillator_line_two, dtype="float"),panel=1, color='red')
		addplots.append(line_plot)

	# print(len(addplots), len(all_pitchfork_lines))
	mpf.plot(function_initial_data, addplot=addplots, type='candle', style="yahoo",figscale=1.2, volume=True)

def findTrend(data):
	global found_trend

	if(data[0] < data[len(data)-1]):
		found_trend = 'uptrend'
		return 'uptrend'
	else:
		found_trend = 'downtrend'
		return 'downtrend'

def findSingleCandleStructure(data):
	open, high, low, close, volume = [round(data[i], CDL_ROUND_DIGITS) for i in range(len(data))]

	patterns = []
	MIN_SHADOW = 10

	MIN_SHADOW_VALUE = MIN_SHADOW * CDL_ROUND_DIGITS

	candle_status = 'bullish' if(close > open) else 'bearish'

	candle_body = round(abs(open - close), CDL_ROUND_DIGITS)
	if(candle_status == 'bearish'):
		upper_shadow = round(abs(open - high), CDL_ROUND_DIGITS)
		lower_shadow = round(abs(close - low), CDL_ROUND_DIGITS)
	elif(candle_status == 'bullish'):
		upper_shadow = round(abs(close - high), CDL_ROUND_DIGITS)
		lower_shadow = round(abs(open - low), CDL_ROUND_DIGITS)

	if(open == close):
		patterns.append('doji')

	if(not('doji' in patterns)):
		if((candle_body < 2*lower_shadow) and (upper_shadow < lower_shadow) and (upper_shadow < MIN_SHADOW_VALUE) and (lower_shadow > candle_body) and (candle_status == 'bullish' or IGNORE_CANDLE_STATUS)):
			patterns.append('hammer')

		if((candle_body < 2*lower_shadow) and (upper_shadow < lower_shadow) and (upper_shadow < MIN_SHADOW_VALUE) and (lower_shadow > candle_body) and (candle_status == 'bearish' or IGNORE_CANDLE_STATUS)):
			patterns.append('hanging_man')

		if((candle_body < 2*upper_shadow) and (upper_shadow > lower_shadow) and (lower_shadow < MIN_SHADOW_VALUE) and (upper_shadow > candle_body) and (candle_status == 'bullish' or IGNORE_CANDLE_STATUS)):
			patterns.append('inverted_hammer')

		if((candle_body < 2*upper_shadow) and (upper_shadow > lower_shadow) and (lower_shadow < MIN_SHADOW_VALUE) and (upper_shadow > candle_body) and (candle_status == 'bearish' or IGNORE_CANDLE_STATUS)):
			patterns.append('shooting_star')

		if((candle_body > upper_shadow) and (candle_body > lower_shadow) and (lower_shadow < MIN_SHADOW_VALUE) and (upper_shadow < MIN_SHADOW_VALUE) and (candle_body > 0.0001)):
			patterns.append('shaven_shadows')

		max_star_body = 5 * (10 ** -CDL_ROUND_DIGITS)
		if((candle_body < max_star_body)):
			if((upper_shadow < candle_body) and (lower_shadow < candle_body) and (not 'hammer' in patterns) and (not 'hanging_man' in patterns) and (not 'inverted_hammer' in patterns) and (not 'shooting_star' in patterns)):
				patterns.append('ideal_star')
			else:
				patterns.append('star')


	# print(candle_body, upper_shadow, lower_shadow, patterns, candle_status)
	return patterns, candle_status, upper_shadow, candle_body, lower_shadow

### At Point Values :-

def findAllTrendLineAtLast():
	global all_last_candle_patterns

	last_candle_position = len(function_initial_data) - 1
	trend_lines_at_last = getLinePointsAtPoint(last_candle_position)

	all_last_candle_patterns['trend_lines'] = trend_lines_at_last
	return trend_lines_at_last

def findAllSupportResistanceAtLast():
	global all_last_candle_patterns

	last_candle_position = len(function_initial_data) - 1
	support_resistance_of_last_candle = getSupportResistanceLinePointsAtPoint(last_candle_position)

	all_last_candle_patterns['support_resistance_lines'] = support_resistance_of_last_candle

	return support_resistance_of_last_candle

def findAllPitchforkAtLast():
	global all_last_candle_patterns

	last_candle_position = len(function_initial_data) - 1
	pitchfork_lines_at_last = getPitchforkLinePointsAtPoint(last_candle_position)

	all_last_candle_patterns['pitchfork_lines'] = pitchfork_lines_at_last

	return pitchfork_lines_at_last

def findAllCandleStickPatternsAtLast():
	global all_candlestick_patterns
	global all_candlestick_predictions
	global all_last_candle_patterns

	# print(function_initial_data.tail(4), len(function_initial_data), SCAN_LENGTH, EXTEND_LENGTH)
	# exit()
	# df = function_initial_data.iloc[:SCAN_LENGTH+EXTEND_LENGTH]
	# df = function_initial_data.tail(SCAN_LENGTH+EXTEND_LENGTH)
	df = function_initial_data
	# df = pd.DataFrame(df)
	# print(df.tail(5))
	# exit()

	data = df

	round_digits = 5

	signal = []
	max_of_min_tail_length = 0.0002
	ratio = 2

	# i -> last candle position
	i = len(function_initial_data) - 1

	# body of candle
	diff_open_close = round(abs(data['open'][i] - data['close'][i]), round_digits)
	
	# candle body height
	diff_open_close = round(abs(data['open'][i] - data['close'][i]), round_digits)

	max_of_min_tail_length = diff_open_close

	vol = round(abs(data['close'][SCAN_LENGTH-1] - data['open'][i]), round_digits)

	trend = findTrend(data['close'][i-5:i])

	n_structure, n_status, n_upper_shadow, n_candle_body, n_lower_shadow = findSingleCandleStructure(data.iloc[i])
	n_minus_one_structure, n_minus_one_status, n_minus_one_upper_shadow, n_minus_one_candle_body, n_minus_one_lower_shadow = findSingleCandleStructure(data.iloc[i-1])
	n_minus_two_structure, n_minus_two_status, n_minus_two_upper_shadow, n_minus_two_candle_body, n_minus_two_lower_shadow = findSingleCandleStructure(data.iloc[i-2])
	n_minus_three_structure, n_minus_three_status, n_minus_three_upper_shadow, n_minus_three_candle_body, n_minus_three_lower_shadow = findSingleCandleStructure(data.iloc[i-3])

	print(n_status, n_structure)
	
	last_I = 0
	considerTweezer = True
	considerCounterBearishAttack = True
	considerCounterBullishAttack = True

	candle_patterns = {}
	patterns = []
	predictions = []


	# print(str(i) + '/' + str(len(df)-50))
	if(len(n_structure) > 0):
		# print('No of Patterns for this candle: ' + str(len(n_structure)))
		# print(n_structure, last_candle_structure)
		for index in range(len(n_structure)):
			plot = False
			# predictions = []
			# patterns = []

			# Predict Patterns
			# Hammer
			if((n_structure[index] == 'hammer') and (trend == 'downtrend') and (not(('shaven_shadows' in n_minus_one_structure) and (n_minus_one_status == 'bearish')))):
				plot = True
				pred = 'bullish'
				pat_name = 'bullish_hammer'
				predictions.append(pred)
				patterns.append(pat_name)
				candle_patterns[pat_name] = pred

			# Inverted Hammer
			if((n_structure[index] == 'inverted_hammer') and (trend == 'downtrend') and (not(('shaven_shadows' in n_minus_one_structure) and (n_minus_one_status == 'bearish')))):
				plot = True
				pred = 'bullish'
				pat_name = 'bullish_inverted_hammer'
				predictions.append(pred)
				patterns.append(pat_name)
				candle_patterns[pat_name] = pred

			# Hanging Man
			if((n_structure[index] == 'hanging_man') and (trend == 'uptrend') and (not(('shaven_shadows' in n_minus_one_structure) and (n_minus_one_status == 'bullish')))):
				plot = True
				pred = 'bearish'
				pat_name = 'bearish_hanging_man'
				predictions.append(pred)
				patterns.append(pat_name)
				candle_patterns[pat_name] = pred


			# Shooting Star
			if((n_structure[index] == 'shooting_star') and (trend == 'uptrend') and (not(('shaven_shadows' in n_minus_one_structure) and (n_minus_one_status == 'bullish')))):
				plot = True
				pred = 'bearish'
				pat_name = 'bearish_shooting_star'
				predictions.append(pred)
				patterns.append(pat_name)
				candle_patterns[pat_name] = pred

			
			# Engulfing
			if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure)):
				# Bullish Engulfing
				if((trend == 'downtrend') and (n_minus_one_status == 'bearish') and (n_status == 'bullish') and (data['open'][i-1] < data['close'][i]) and (data['close'][i-1] > data['open'][i])):
					plot = True 
					pred = 'bullish'
					pat_name = 'bullish_engulfing'
					predictions.append(pred)
					patterns.append(pat_name)
					candle_patterns[pat_name] = pred


				# Bearish Engulfing
				if((trend == 'uptrend') and (n_minus_one_status == 'bullish') and (n_status == 'bearish') and (data['open'][i-1] > data['close'][i]) and (data['close'][i-1] < data['open'][i])):
					plot = True 
					pred = 'bearish'
					pat_name = 'bearish_engulfing'
					predictions.append(pred)
					patterns.append(pat_name)
					candle_patterns[pat_name] = pred


			# Dark Cloud
			if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure) and (trend == 'uptrend') and (n_minus_one_status == 'bullish') and (n_status == 'bearish')):
				n_minus_one_half_point = (data['close'][i-1] + data['open'][i-1]) / 3
				if((data['open'][i-1] < data['close'][i]) and (data['close'][i-1] < data['open'][i]) and (data['close'][i] < n_minus_one_half_point)):
					plot = True 
					pred = 'bearish'
					pat_name = 'dark_cloud'
					predictions.append(pred)
					patterns.append(pat_name)
					candle_patterns[pat_name] = pred

			
			# Piercing
			if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure) and (trend == 'downtrend') and (n_minus_one_status == 'bearish') and (n_status == 'bullish')):
				n_minus_one_half_point = (data['close'][i-1] + data['open'][i-1]) / 2
				if((data['open'][i-1] > data['close'][i]) and (data['close'][i-1] > data['open'][i]) and (data['close'][i] > n_minus_one_half_point)):
					plot = True 
					pred = 'bullish'
					pat_name = 'Piercing'
					predictions.append(pred)
					patterns.append(pat_name)
					candle_patterns[pat_name] = pred

			
			# Morning Star
			if((trend == 'downtrend') and (n_minus_two_status == 'bearish') and (n_minus_one_status == 'bearish') and (n_status == 'bullish')):
				if(('shaven_shadows' in n_minus_two_structure) and (n_minus_one_candle_body < MAX_STAR_BODY)  and (n_minus_one_candle_body != 0) and (n_structure[index] == 'shaven_shadows')):
					if((data['open'][i-1]) < (data['close'][i]) and (data['open'][i-1] < data['close'][i-2])  and (data['close'][i] < data['open'][i-2])):
						plot = True 
						pred = 'bullish'
						pat_name = 'morning_star'
						predictions.append(pred)
						patterns.append(pat_name)
						candle_patterns[pat_name] = pred


			# Evening Star
			if((trend == 'uptrend') and (n_minus_two_status == 'bullish') and (n_minus_one_status == 'bullish') and (n_status == 'bearish')):
				if(('shaven_shadows' in n_minus_two_structure) and (n_minus_one_candle_body < MAX_STAR_BODY)  and (n_minus_one_candle_body != 0) and (n_structure[index] == 'shaven_shadows')):
					if((data['close'][i-1]) > (data['open'][i]) and (data['open'][i-1] > data['close'][i-2])  and (data['close'][i] > data['open'][i-2])):
						plot = True
						pred = 'bearish'
						pat_name = 'evening_star'
						predictions.append(pred)
						patterns.append(pat_name)
						candle_patterns[pat_name] = pred
			
			# Morning doji
			if((trend == 'downtrend') and ('doji' in n_minus_one_structure) and (n_minus_two_status == 'bearish') and (n_minus_one_status == 'bearish') and (n_status == 'bullish')):
				if(('shaven_shadows' in n_minus_two_structure) and (n_structure[index] == 'shaven_shadows')):
					if((data['open'][i-1]) < (data['close'][i]) and (data['open'][i-1] < data['close'][i-2])  and (data['close'][i] < data['open'][i-2])):
						plot = True 
						pred = 'bullish'
						pat_name = 'morning_doji'
						predictions.append(pred)
						patterns.append(pat_name)
						candle_patterns[pat_name] = pred
			
			# Evening doji
			if((trend == 'uptrend') and ('doji' in n_minus_one_structure) and (n_minus_two_status == 'bullish') and (n_minus_one_status == 'bullish') and (n_status == 'bearish')):
				if(('shaven_shadows' in n_minus_two_structure) and (n_structure[index] == 'shaven_shadows')):
					if((data['close'][i-1]) > (data['open'][i]) and (data['open'][i-1] > data['close'][i-2])  and (data['close'][i] > data['open'][i-2])):
						plot = True
						pred = 'bearish'
						pat_name = 'evening_doji'
						predictions.append(pred)
						patterns.append(pat_name)
						candle_patterns[pat_name] = pred
			
			# Harami 
			if(('shaven_shadows' in n_minus_one_structure) and ((n_structure[index] == 'star') or (n_structure[index] == 'ideal_star'))):
				# Bearish Harami
				if((trend == 'uptrend') and (n_minus_one_status == 'bullish') and (n_status == 'bearish')):
					if((data['open'][i-1] < data['high'][i]) and (data['open'][i-1] < data['low'][i]) and (data['close'][i-1] > data['high'][i]) and (data['close'][i-1] > data['low'][i])):
						plot = True 
						pred = 'bearish'
						pat_name = 'bearish_harami'
						predictions.append(pred)
						patterns.append(pat_name)
						candle_patterns[pat_name] = pred

				# Bullish Harami
				if((trend == 'downtrend') and (n_minus_one_status == 'bearish') and (n_status == 'bullish')):
					if((data['open'][i-1] > data['high'][i]) and (data['open'][i-1] > data['low'][i]) and (data['close'][i-1] < data['high'][i]) and (data['close'][i-1] < data['low'][i])):
						plot = True 
						pred = 'bullish'
						pat_name = 'bullish_harami'
						predictions.append(pred)
						patterns.append(pat_name)
						candle_patterns[pat_name] = pred
			
			# Harami Cross
			if(('shaven_shadows' in n_minus_one_structure) and (n_structure[index] == 'doji')):
				# Bearish Harami Cross
				if((trend == 'uptrend') and (n_minus_one_status == 'bullish')):
					if((data['open'][i-1] < data['high'][i]) and (data['open'][i-1] < data['low'][i]) and (data['close'][i-1] > data['high'][i]) and (data['close'][i-1] > data['low'][i])):
						plot = True 
						pred = 'bearish'
						pat_name = 'bearish_harami_cross'
						predictions.append(pred)
						patterns.append(pat_name)
						candle_patterns[pat_name] = pred

				# Bullish Harami Cross
				if((trend == 'downtrend') and (n_minus_one_status == 'bearish')):
					if((data['open'][i-1] > data['high'][i]) and (data['open'][i-1] > data['low'][i]) and (data['close'][i-1] < data['high'][i]) and (data['close'][i-1] < data['low'][i])):
						plot = True 
						pred = 'bullish'
						pat_name = 'bullish_harami_cross'
						predictions.append(pred)
						patterns.append(pat_name)
						candle_patterns[pat_name] = pred

			# Tweezers
			if((considerTweezer == True) and ('shaven_shadows' in n_minus_one_structure)):
				# Bearish Tweezer Top
				if((n_minus_one_status == 'bullish') and (n_status == 'bearish')):
					if((data['high'][i-1] == data['high'][i]) and (trend == 'uptrend')):
						plot = True 
						pred = 'bearish'
						pat_name = 'bearish_tweezer_top'
						predictions.append(pred)
						patterns.append(pat_name)
						candle_patterns[pat_name] = pred
						considerTweezer = False

				# Bullish Tweezer Bottom
				if((n_minus_one_status == 'bearish') and (n_status == 'bullish')):
					if((data['low'][i-1] == data['low'][i]) and (trend == 'downtrend')):
						plot = True 
						pred = 'bullish'
						pat_name = 'bullish_tweezer_bottom'
						predictions.append(pred)
						patterns.append(pat_name)
						candle_patterns[pat_name] = pred
						considerTweezer = False

			# Three Black Crows
			if((trend == 'uptrend') and (n_status == 'bearish') and (n_minus_one_status == 'bearish') and (n_minus_two_status == 'bearish') and (n_minus_three_status == 'bullish')):
				if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure) and ('shaven_shadows' in n_minus_two_structure)):
					plot = True 
					pred = 'bearish'
					pat_name = 'three_black_crows'
					predictions.append(pred)
					patterns.append(pat_name)
					candle_patterns[pat_name] = pred

			# Three White Soldiers
			if((trend == 'downtrend') and (n_status == 'bullish') and (n_minus_one_status == 'bullish') and (n_minus_two_status == 'bullish') and (n_minus_three_status == 'bearish')):
				if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure) and ('shaven_shadows' in n_minus_two_structure)):
					plot = True 
					pred = 'bullish'
					pat_name = 'three_white_soldiers'
					predictions.append(pred)
					patterns.append(pat_name)
					candle_patterns[pat_name] = pred


	all_candlestick_patterns = patterns
	all_candlestick_predictions = predictions
	all_last_candle_patterns['candle_sticks'] = candle_patterns

	return candle_patterns

def findExpectedProfitPointsAndWeight(last_candle_close, stat, ar_pts, weight):
	b_exp_profit_pts = float(0)
	s_exp_profit_pts = float(0)
	buy_weight = 0
	sell_weight = 0

	cprint('weight', 'blue', 'on_white')
	cprint(weight, 'blue', 'on_white')

	symbol_pip = mt5.symbol_info(selected_symbol).point

	
	nearest_point = MAXIMUM_CONSIDERABLE_DISTANCE_BETWEEN_LINE_AND_PRICE
	# nearest_point = 0.001

	if(len(ar_pts) > 1):
		if(stat == 'Bullish'):
			cprint('Bullish', 'blue', 'on_white')

			for i in range(len(ar_pts)):

				if(ar_pts[i] > last_candle_close):
					cprint('YES ar_pts[i] > last_candle_close', 'blue', 'on_white')
					if(abs(ar_pts[i] - last_candle_close) < nearest_point):
						cprint('YES abs(ar_pts[i] - last_candle_close) < nearest_', 'blue', 'on_white')
						exp_profit_pts = abs(last_candle_close - ar_pts[i-1])
						cprint(exp_profit_pts, 'blue', 'on_white')
						cprint(abs(last_candle_close - ar_pts[i-1]), 'blue', 'on_white')
						if(exp_profit_pts >= (symbol_pip * NUMBER_OF_PIPS_BETWEEN_NEXT_LINE_AND_LAST_CANDLE_CLOSE_PRICE)):
							sell_weight = sell_weight + weight
							s_exp_profit_pts = exp_profit_pts
							cprint('YES exp_profit_pts >= NUMBER_OF_PIPS_BETWEEN_NEXT_L', 'blue', 'on_white')

						break

		if(stat == 'Bearish'):
			cprint('Bearish', 'blue', 'on_white')

			for i in range(len(ar_pts)): # ar_pts is in Ascending order

				if(len(ar_pts) > i+1):
					if(ar_pts[i+1] > last_candle_close): # if next point is greater than last candle close
						cprint('YES ar_pts[i+1] > last_candle_cl', 'blue', 'on_white')
						if(ar_pts[i] < last_candle_close): # and current point is lesser thatn last candle close
							cprint('YES ar_pts[i] < last_candle_cl', 'blue', 'on_white')
							if(abs(ar_pts[i] - last_candle_close) < nearest_point): # current candle is in acceptable distance
								cprint('YES abs(ar_pts[i] - last_candle_close) < neares', 'blue', 'on_white')
								exp_profit_pts = abs(ar_pts[i+1] - last_candle_close)
								cprint(exp_profit_pts, 'blue', 'on_white')
								if(exp_profit_pts >= (symbol_pip * NUMBER_OF_PIPS_BETWEEN_NEXT_LINE_AND_LAST_CANDLE_CLOSE_PRICE)):
									buy_weight = buy_weight + weight
									b_exp_profit_pts = exp_profit_pts
									cprint('YES', 'blue', 'on_white')

								break

	
	return b_exp_profit_pts, s_exp_profit_pts, buy_weight, sell_weight

def takeTradeDecision():
	global selected_symbol
	global trade_log
	global TRADE_WITH_TREND

	log = ''
	
	all = all_last_candle_patterns

	william_r = all['oscillators']['william_r']
	rsi = all['oscillators']['rsi']
	stochastic = all['oscillators']['stochastic']
	obv = all['oscillators']['obv']

	trend_lines = np.array(all['trend_lines'])
	trend_lines = list(filter(None, trend_lines))
	support_resistance_lines = np.array(all['support_resistance_lines'])
	support_resistance_lines = list(filter(None, support_resistance_lines))
	pitchfork_lines = np.array(all['pitchfork_lines'])
	pitchfork_lines = list(filter(None, pitchfork_lines))

	candle_sticks = all['candle_sticks']
	# candle_sticks = {'bullish_inverted_hammer': 'bullish'}
	# print(candle_sticks, all_last_candle_patterns)

	buy_weight = 0
	sell_weight = 0

	asc_trend_lines = np.sort(np.array(trend_lines))
	asc_sup_res_lines = np.sort(np.array(support_resistance_lines))
	asc_pitchfork_lines = np.sort(np.array(pitchfork_lines))

	last_candle_bull_or_bear = isPointBullishOrBearish(SCAN_LENGTH+EXTEND_LENGTH-1)
	last_candle = function_initial_data.tail(1)
	last_candle_close = last_candle['close'].iloc[-1]
	last_candle_open = last_candle['open'].iloc[-1]
	last_candle_high = last_candle['high'].iloc[-1]
	last_candle_low = last_candle['low'].iloc[-1]

	candle_weight = 1.5

	for cdl_type in candle_sticks:
		val = candle_sticks[cdl_type]
		if(val == 'bullish'):
			buy_weight = buy_weight + candle_weight
			log = log + ' ' + str(val)
		if(val == 'bearish'):
			sell_weight = sell_weight + candle_weight
			log = log + ' ' + str(val)
		cprint(val, 'red', 'on_white')
		cprint(cdl_type, 'red', 'on_white')

	cprint(candle_sticks, 'red', 'on_white')

	# print(last_candle_bull_or_bear)

	# # William R
	# if(william_r > 0.5):
	# 	sell_weight = sell_weight + 1
	# 	log = log + ' william_r'
	# elif(william_r < 0.5):
	# 	buy_weight = buy_weight + 1
	# 	log = log + ' william_r'

	# # RSI
	# if(rsi > 0.5):
	# 	sell_weight = sell_weight + 1
	# 	log = log + ' rsi'

	# elif(rsi < 0.5):
	# 	buy_weight = buy_weight + 1
	# 	log = log + ' rsi'


	# # Stochastic
	# if(stochastic > 0.5):
	# 	sell_weight = sell_weight + 1
	# elif(stochastic < 0.5):
	# 	buy_weight = buy_weight + 1


	# Trend Line
	exp_trend_pft_pts = 0
	b_exp_trend_pft_pts, s_exp_trend_pft_pts, trend_b_weight, trend_s_weight = findExpectedProfitPointsAndWeight(last_candle_close, last_candle_bull_or_bear, asc_trend_lines, TREND_LINE_WEIGHT)
	buy_weight = buy_weight + trend_b_weight
	sell_weight = sell_weight + trend_s_weight
	if((trend_s_weight > 0) or (trend_b_weight > 0)):
		log = log + ' Trend Line |'

	# PitchFork Line
	exp_pitch_pft_pts = 0
	b_exp_pitch_pft_pts, s_exp_pitch_pft_pts, pitch_b_weight, pitch_s_weight = findExpectedProfitPointsAndWeight(last_candle_close, last_candle_bull_or_bear, asc_pitchfork_lines, PITCHFORK_LINE_WEIGHT)
	buy_weight = buy_weight + pitch_b_weight
	sell_weight = sell_weight + pitch_s_weight
	if((trend_s_weight > 0) or (pitch_b_weight > 0)):
		log = log + ' Pitchfork Line |'
	
	# Support Resistance Line
	exp_sup_res_pft_pts = 0
	b_exp_sup_res_pft_pts, s_exp_sup_res_pft_pts, sup_res_b_weight, sup_res_s_weight = findExpectedProfitPointsAndWeight(last_candle_close, last_candle_bull_or_bear, asc_trend_lines, SUPPORT_RESISTANCE_WEIGHT)
	buy_weight = buy_weight + sup_res_b_weight
	sell_weight = sell_weight + sup_res_s_weight
	if((trend_s_weight > 0) or (sup_res_b_weight > 0)):
		log = log + ' Support Resistance Line |'

	# CandleStick Pattern


	b_total_expected_pft = b_exp_trend_pft_pts + b_exp_pitch_pft_pts + b_exp_sup_res_pft_pts
	s_total_expected_pft = s_exp_trend_pft_pts + s_exp_pitch_pft_pts + s_exp_sup_res_pft_pts	

	b_avg_expected_pft = sum([b_exp_trend_pft_pts, b_exp_pitch_pft_pts, b_exp_sup_res_pft_pts]) / 3
	s_avg_expected_pft = sum([s_exp_trend_pft_pts, s_exp_pitch_pft_pts, s_exp_sup_res_pft_pts]) / 3
	

	# print(b_total_expected_pft, s_total_expected_pft, b_avg_expected_pft, s_avg_expected_pft)
	# print(buy_weight, sell_weight)
	# exit()

	# print(buy_weight, sell_weight, exp_trend_pft_pts, exp_pitch_pft_pts, exp_sup_res_pft_pts)
	# print(sum([exp_trend_pft_pts, exp_pitch_pft_pts, exp_sup_res_pft_pts])/3, total_expected_pft)

	if(found_trend == 'uptrend'):
		buy_weight = buy_weight + 0.5
		log = log + ' UPtrend |'

	if(found_trend == 'downtrend'):
		sell_weight = sell_weight + 0.5
		log = log + ' Downtrend |'

	# signal_strength = 1
	signal_strength = 1.5
	# sell_weight = 9
	# gowtham
	# if(sell_weight != buy_weight):

	TRADE_WITH_TREND_STATUS = False

	if(TRADE_WITH_TREND == True):
		if((found_trend == 'uptrend') and (buy_weight > sell_weight)):
			TRADE_WITH_TREND_STATUS = True 
		if((found_trend == 'downtrend') and (sell_weight > buy_weight)):
			TRADE_WITH_TREND_STATUS = True 


	if(abs(sell_weight - buy_weight) > signal_strength and (TRADE_WITH_TREND and TRADE_WITH_TREND_STATUS)):

		trade_log = open('trade_log.txt', 'a')
		trade_log.write("sell_weight = " + str(sell_weight) + " | buy_weight = " + str(buy_weight) + " | diff = " + str(abs(sell_weight - buy_weight)) + "\n")
		trade_log.write(log + "\n")
		trade_log.close()

		trade_type = ''
		lot = 0.01
		stop_loss = ''
		trailing_stop_loss = ''
		take_profit = ''
		stop_loss_pips = ''
		trailing_stop_loss_pips = ''
		take_profit_pips = ''

		symbol_pip = mt5.symbol_info(selected_symbol).point


		if(timeframe == mt5.TIMEFRAME_M1):
			stop_loss_pips = symbol_pip * stop_loss_take_profit['1_minute']['stop_loss']
			# trailing_stop_loss = stop_loss_take_profit['1_minute']['trailing_stop_loss']
		if(timeframe == mt5.TIMEFRAME_M2):
			stop_loss_pips = symbol_pip * stop_loss_take_profit['2_minute']['stop_loss']
			trailing_stop_loss_pips = symbol_pip * stop_loss_take_profit['2_minute']['trailing_stop_loss']
		if(timeframe == mt5.TIMEFRAME_M3):
			stop_loss_pips = symbol_pip * stop_loss_take_profit['3_minute']['stop_loss']
			trailing_stop_loss_pips = symbol_pip * stop_loss_take_profit['3_minute']['trailing_stop_loss']
		if(timeframe == mt5.TIMEFRAME_M5):
			stop_loss_pips = symbol_pip * stop_loss_take_profit['5_minute']['stop_loss']
			trailing_stop_loss_pips = symbol_pip * stop_loss_take_profit['5_minute']['trailing_stop_loss']
		if(timeframe == mt5.TIMEFRAME_M15):
			stop_loss_pips = symbol_pip * stop_loss_take_profit['15_minute']['stop_loss']
		if(timeframe == mt5.TIMEFRAME_M30):
			stop_loss_pips = symbol_pip * stop_loss_take_profit['30_minute']['stop_loss']
		if(timeframe == mt5.TIMEFRAME_H1):
			stop_loss_pips = symbol_pip * stop_loss_take_profit['16385_minute']['stop_loss']
			
		
		if(sell_weight > buy_weight):
			trade_type = 'sell'
		if(sell_weight < buy_weight):
			trade_type = 'buy'

		print(last_candle_close, last_candle_open, last_candle_close > last_candle_open)
		print('============================================================================================================')

		if(last_candle_close > last_candle_open): # last candle is Bullish
			print('Last Candle Position is: ' + 'Bullish')
			if(trade_type == 'buy'):
				# take_profit = last_candle_close + take_profit_points
				stop_loss = last_candle_close - stop_loss_pips
			if(trade_type == 'sell'):
				# take_profit = last_candle_close - take_profit_points
				stop_loss = last_candle_close + stop_loss_pips

		if(last_candle_close < last_candle_open): # last candle is Bearish
			print('Last Candle Position is: ' + 'Bearish')
			if(trade_type == 'buy'):
				# take_profit = last_candle_close + take_profit_points
				stop_loss = last_candle_close - stop_loss_pips
			if(trade_type == 'sell'):
				# take_profit = last_candle_close - take_profit_points
				stop_loss = last_candle_close + stop_loss_pips

		if(last_candle_close == last_candle_open): # last candle is Doji
			print('Last Candle Position is: ' + 'Doji')
			# take_profit_points = (last_candle_volume * ( 0.00001 * 10 ))
			# stop_loss_points = take_profit_points / 2
			
			if(trade_type == 'buy'):
				# take_profit = last_candle_close + take_profit_points
				stop_loss = last_candle_close - stop_loss_pips
			if(trade_type == 'sell'):
				# take_profit = last_candle_close - take_profit_points
				stop_loss = last_candle_close + stop_loss_pips

		cprint('stop_loss', 'white', 'on_red')
		cprint(stop_loss, 'white', 'on_red')

		stop_loss = round(float(stop_loss), 5)
		take_profit = float(0)
		take_profit = round(float(take_profit), 5)

		request = getRequest(trade_type, stop_loss, take_profit, lot)

		cprint('request is ' , 'white', 'on_magenta')
		cprint(request , 'white', 'on_magenta')


		if(request != False):
			# trade_log = open('trade_log.txt', 'a')
			# trade_log.write(request)
			# trade_log.close()
			openTrade(request)
			cprint('open Trade is happening', 'white', 'on_green')
		else:
			cprint('Request is False', 'white', 'on_red')


		print('last_candle_close, take_profit, stop_loss')
		print(last_candle_close, take_profit, stop_loss)
		# print(request)

		# print('TRADE OPENED')
		# print(trade_type, stop_loss, take_profit, lot)
	else:
		print(sell_weight, buy_weight)
		cprint('NOT OPENED', 'white', 'on_red')

	# closePreviousTrades()

	# exit()

	# print(all)
	# print(all['trend_lines'])
	# print(all['support_resistance_lines'])
	# print(all['pitchfork_lines'])
	# print(all['oscillators'])

	# exit()


def getAllAtPointValue():	
	getMinimaPoints()
	getMaximaPoints()
	getExtremePoints()

	# global all_last_candle_patterns

	## Trend Line
	getAllLinesForExtremePoints()
	findAllTrendLineAtLast()

	## Support Resistance
	getSupportAndResistanceLines()
	findAllSupportResistanceAtLast()

	## Pitchfork
	getPitchforkPoints()
	getPitchforkLines()
	findAllPitchforkAtLast()

	## Candle Pattern 
	findAllCandleStickPatternsAtLast() 


	# print(all_last_candle_patterns)

if __name__ == "__main__":
	# Login Metatrader account
	initializeMetaTrader()

	getChartData()
	getAllAtPointValue()

	selectGraph = ['lines', 'points', 'support_resistance', 'pitchfork']
	plotCandleStickGraph(selectGraph)


	exit()



