

def getRequest(trade_type, stop_loss, take_profit, lot):

	if not mt5.initialize(login=MT_login, server=MT_server,password=MT_password):
		print("initialize() failed, error code =",mt5.last_error())
		return False

	symbol_info = mt5.symbol_info(selected_symbol)

	if symbol_info is None:
		print(selected_symbol, "not found, can not call order_check()")
		mt5.shutdown()
		return False


	# if the symbol is unavailable in MarketWatch, add it
	if symbol_info is not None:
		if not symbol_info.visible:
			print(selected_symbol, "is not visible, trying to switch on")
			if not mt5.symbol_select(selected_symbol,True):
				print("symbol_select({}}) failed, exit",selected_symbol)
				mt5.shutdown()
				return False

	point = mt5.symbol_info(selected_symbol).point

	# to create new order
	action = mt5.TRADE_ACTION_DEAL
	# lot = 0.01

	order_type = ''
	if(trade_type == 'buy'):
		order_type = mt5.ORDER_TYPE_BUY
	if(trade_type == 'sell'):
		order_type = mt5.ORDER_TYPE_SELL


	# ask price for buying
	price = mt5.symbol_info_tick(selected_symbol).ask
	# bid price for selling
	price = mt5.symbol_info_tick(selected_symbol).bid

	# stop_loss = price - 100 * point
	# take_profit = price + 100 * point

	deviation = 20 # tolerance to bid / ask price

	magic = 12345678 # EA ID. unique

	comment = 'python script open'

	type_time = mt5.ORDER_TIME_GTC

	type_filling = mt5.ORDER_FILLING_IOC
	# "type_filling" = mt5.ORDER_FILLING_FOK
	# "type_filling" = mt5.ORDER_FILLING_RETURN

	request = {
		"action": action,
		"symbol": selected_symbol,
		"volume": lot,
		"type": order_type,
		"price": price,
		"sl": stop_loss,
		"tp": take_profit,
		"deviation": deviation,
		"magic": magic,
		"comment": comment,
		"type_time": type_time,
		"type_filling": type_filling,
	}

	# result = mt5.order_send(request)

	return request

def openTrade(request):
	global future_close_positions
	global future_close_positions_log

	# send a trading request
	result = mt5.order_send(request)

	# check the execution result
	# print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation))
	cprint("1. order_send()", 'white', 'on_green')
	cprint(mt_error_codes[result.retcode], 'white', 'on_magenta')

	if result.retcode != mt5.TRADE_RETCODE_DONE:
		"""
		print("2. order_send failed, retcode={}".format(result.retcode))
		# request the result as a dictionary and display it element by element
		result_dict=result._asdict()
		for field in result_dict.keys():
			print("   {}={}".format(field,result_dict[field]))
			if this is a trading request structure, display it element by element as well
			if field=="request":
				traderequest_dict=result_dict[field]._asdict()
				for tradereq_filed in traderequest_dict:
					print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
		"""
		print("shutdown() and quit")
	else:
		timezone = pytz.timezone("Etc/GMT-3") # toggles according to season (NYSE) ( summer, winter )
		now = datetime.now(timezone)
		current_timestamp = datetime.timestamp(now)

		# gowtham
		# close_timestamp = int(current_timestamp) + int(no_of_seconds_for_timestamp_candle[str(timeframe) + '_minute']) - 30
		close_timestamp = int(current_timestamp) + (int(no_of_seconds_for_timestamp_candle[str(timeframe) + '_minute']) * 3) - 30
		
		positionValue = result.order

		# print(request, request['type'])
		positionType = request['type']

		# hasTrailingStopLoss = False

		# new_future_close_positions = { 'timeToClose': close_timestamp, 'positionValue': positionValue, 'positionType': positionType, 'timeFrame': timeframe, 'hasTrailingStopLoss': hasTrailingStopLoss, 'symbol': selected_symbol }

		# print('new_future_close_positions')
		# print(new_future_close_positions)

		# future_close_positions.append(new_future_close_positions)
		# future_close_positions_log.append(new_future_close_positions)

		# if(PLOT_GRAPH_AFTER_OPEN_POSITION == True):
		# 	print('PLOTING GRAPH...')
		# 	selectGraph = ['lines', 'points', 'support_resistance', 'pitchfork']
		# 	plotCandleStickGraph(selectGraph)


	return True

def closeTrade(positionValue, positionType):
	global future_close_positions

	cprint(positionValue, 'red', 'on_yellow')
	
	# create a close request
	position_id = positionValue

	# if opened position is SELL , price is bid and request Type is BUY
	price=mt5.symbol_info_tick(selected_symbol).bid
	requestType = mt5.ORDER_TYPE_BUY
	if(positionType == 0): # if opened position is BUY , price is ask and request Type is SELL
		price=mt5.symbol_info_tick(selected_symbol).ask
		requestType = mt5.ORDER_TYPE_SELL

	request={
		"action": mt5.TRADE_ACTION_DEAL,
		"symbol": selected_symbol,
		"volume": lot,
		"type": requestType,
		"position": position_id,
		"price": price,
		"deviation": deviation,
		"magic": magic,
		"comment": "python script close",
		"type_time": mt5.ORDER_TIME_GTC,
		"type_filling": mt5.ORDER_FILLING_IOC,
	}

	# send a trading request
	result=mt5.order_send(request)

	cprint(request, 'green', 'on_white')
	cprint(result, 'magenta', 'on_white')

	# check the execution result
	print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,selected_symbol,lot,price,deviation))

	cprint(mt_error_codes[result.retcode], 'white', 'on_magenta')


	cprint('Removing position Value : ' + str(positionValue), 'white', 'on_magenta')
	
	if result.retcode == mt5.TRADE_RETCODE_DONE:
		# future_close_positions = future_close_positions.filter(lambda position: position.positionValue != positionValue)
		future_close_positions = [position for position in future_close_positions if position['positionValue'] != positionValue]

	if result.retcode != mt5.TRADE_RETCODE_DONE:
		cprint("4. order_send failed", 'white', 'on_red')
		print("   result",result)

	else:
		print("4. position #{} closed, {}".format(position_id,result))
		"""
		# request the result as a dictionary and display it element by element
		result_dict=result._asdict()
		for field in result_dict.keys():
			print("   {}={}".format(field,result_dict[field]))
			# if this is a trading request structure, display it element by element as well
			if field=="request":
				traderequest_dict=result_dict[field]._asdict()
				for tradereq_filed in traderequest_dict:
					print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
		"""

def modifyTrailingStopLossTrade(position, live_profit, previous_stop_loss):
	global future_close_positions

	profit = live_profit

	symbol_info = mt5.symbol_info(selected_symbol)
	symbol_info_point = symbol_info.point 
	

	# create a close request
	position_id = position['positionValue']
	positionValue = position['positionValue']
	positionType = position['positionType']
	
	# if opened position is SELL , price is bid and request Type is BUY
	price=mt5.symbol_info_tick(selected_symbol).bid
	requestType = mt5.ORDER_TYPE_BUY
	if(positionType == 0): # if opened position is BUY , price is ask and request Type is SELL
		price=mt5.symbol_info_tick(selected_symbol).ask
		requestType = mt5.ORDER_TYPE_SELL


	take_profit = float(0)
	take_profit = round(float(take_profit), 5)

	symbol_pip = mt5.symbol_info(selected_symbol).point
	

	if(timeframe == mt5.TIMEFRAME_M1):
		stop_loss_pips = symbol_pip * stop_loss_take_profit['1_minute']['stop_loss']
		trailing_stop_loss = stop_loss_take_profit['1_minute']['trailing_stop_loss']
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
		

	# # if opened position is SELL , price is bid and request Type is BUY
	# stop_loss = price + stop_loss_pips
	# if(positionType == 0): # if opened position is BUY , price is ask and request Type is SELL
	# 	stop_loss = price - stop_loss_pips

	# # if opened position is SELL , price is bid and request Type is BUY
	# stop_loss = abs(float(price + profit))
	# if(positionType == 0): # if opened position is BUY , price is ask and request Type is SELL
	# 	stop_loss = abs(float(price - profit))

	# # if opened position is SELL , price is bid and request Type is BUY
	# stop_loss = abs(float(price - profit))
	# if(positionType == 0): # if opened position is BUY , price is ask and request Type is SELL
	# 	stop_loss = abs(float(price + profit))

	modificationIsProfitable = False

	stop_loss = float(0)
	new_stop_loss = float(0)

	profit_pips = profit * 100

	# symbol_info_profit_point = abs(symbol_info_point * profit_pips)
	symbol_info_profit_point = abs(symbol_info_point * trailing_stop_loss)

	if('JPY' in selected_symbol):
		symbol_info_profit_point = round(symbol_info_profit_point, 3)
	else:
		symbol_info_profit_point = round(symbol_info_profit_point, 5)

	if(positionType == 1): # if opened position is SELL
		if(profit_pips > 0): # profit
			new_stop_loss = price - ( symbol_info_profit_point ) + stop_loss_pips
			
		if(profit_pips < 0): # loss
			new_stop_loss = price + ( symbol_info_profit_point ) + stop_loss_pips
			
		if(not ((profit_pips > 0) or (profit_pips < 0))): # not profit, not loss
			new_stop_loss = price + stop_loss_pips 

		if(new_stop_loss < previous_stop_loss):
			stop_loss = new_stop_loss
			modificationIsProfitable = True
	
	if(positionType == 0): # if opened position is BUY
		if(profit_pips > 0): # profit
			new_stop_loss = price + ( symbol_info_profit_point ) - stop_loss_pips
			
		if(profit_pips < 0): # loss
			new_stop_loss = price - ( symbol_info_profit_point ) - stop_loss_pips
			
		if(not ((profit_pips > 0) or (profit_pips < 0))): # not profit, not loss
			new_stop_loss = price - stop_loss_pips 

		if(new_stop_loss > previous_stop_loss):
			stop_loss = new_stop_loss
			modificationIsProfitable = True

	if('JPY' in selected_symbol):
		# cprint('has JPY 333333333333', 'blue', 'on_magenta')
		stop_loss = round(stop_loss, 3)
	else:
		# cprint('DOES NOT HAS has JPY 5555555555', 'blue', 'on_magenta')
		stop_loss = round(stop_loss, 5)

	# cprint(modificationIsProfitable, 'blue', 'on_white')
	# cprint('new_stop_loss', 'blue', 'on_magenta')
	# cprint(new_stop_loss, 'blue', 'on_magenta')
	# cprint('stop_loss', 'blue', 'on_red')
	# cprint(stop_loss, 'blue', 'on_white')
	# cprint('previous_stop_loss', 'blue', 'on_red')
	# cprint(previous_stop_loss, 'blue', 'on_white')
	# cprint('symbol_info_point * profit_pips', 'blue', 'on_red')
	# cprint(symbol_info_point * profit_pips, 'blue', 'on_white')
	# cprint('symbol_info_point', 'blue', 'on_red')
	# cprint(symbol_info_point, 'blue', 'on_white')
	# cprint('STOP LOSS ____________________________________', 'blue', 'on_white')

	if(not modificationIsProfitable):
		return False 
	
	request={
		# "action": mt5.TRADE_ACTION_DEAL,
		# "action": mt5.TRADE_ACTION_MODIFY,
		"action": mt5.TRADE_ACTION_SLTP,
		"symbol": selected_symbol,
		"volume": lot,
		"type": requestType,
		"position": position_id,
		"price": price,
		"sl": stop_loss,
		"tp": take_profit,
		"deviation": deviation,
		"magic": magic,
		"comment": "python script close",
		"type_time": mt5.ORDER_TIME_GTC,
		# "type_filling": mt5.ORDER_FILLING_IOC,
		# "type_filling": mt5.ORDER_FILLING_RETURN,
		"type_filling": mt5.ORDER_FILLING_FOK,
		"ENUM_ORDER_STATE": mt5.ORDER_FILLING_RETURN,
	}

	# send a trading request
	result=mt5.order_send(request)

	# check the execution result
	# print("3. Modify position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,selected_symbol,lot,price,deviation))

	# cprint(mt_error_codes[result.retcode], 'white', 'on_magenta')


	# cprint('Modifing position Value : ' + str(positionValue), 'white', 'on_magenta')
	
	# future_close_positions = future_close_positions.filter(lambda position: position.positionValue != positionValue)
	# future_close_positions = [position for position in future_close_positions if position['positionValue'] != positionValue]

	if result.retcode != mt5.TRADE_RETCODE_DONE:
		cprint("4. order_send modification failed", 'white', 'on_red')
		# print("   result",result)

	else:
		print("4. position #{} ,modified, {}".format(position_id,result))
		"""
		# request the result as a dictionary and display it element by element
		result_dict=result._asdict()
		for field in result_dict.keys():
			print("   {}={}".format(field,result_dict[field]))
			# if this is a trading request structure, display it element by element as well
			if field=="request":
				traderequest_dict=result_dict[field]._asdict()
				for tradereq_filed in traderequest_dict:
					print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
		"""


def closePreviousTrades():
	# getAllPositions()

	# cprint(all_open_positions_from_market, 'white', 'on_red')
	# if(len(all_open_positions_from_market) > 0):
	# 	exit()
	
	# print(future_close_positions)

	timezone = pytz.timezone("Etc/GMT-3") # toggles according to season (NYSE) ( summer, winter )
	now = datetime.now(timezone)
	current_timestamp = datetime.timestamp(now)

	for position in future_close_positions:
		if(position['symbol'] == selected_symbol):
			cprint(str(position['timeToClose']) + '    ' + str(current_timestamp + 1), 'white', 'on_red')
			if(position['timeToClose'] <= (current_timestamp + 1)):
				cprint('GOING TO CLOSE TRADE ', 'white', 'on_magenta')
				cprint(position, 'white', 'on_magenta')
				closeTrade(position['positionValue'], position['positionType'])

	# if(len(future_close_positions) > 0):
	# 	cprint('REMAINING OPEN POSITIONS ARE :', 'red', 'on_yellow')
	# 	cprint(future_close_positions, 'red', 'on_yellow')

def modifyPreviousTrades():
	getAllPositions()

	# cprint(all_open_positions_from_market, 'white', 'on_red')
	# if(len(all_open_positions_from_market) > 0):
	# 	exit()
	
	# print(future_close_positions)

	timezone = pytz.timezone("Etc/GMT-3") # toggles according to season (NYSE) ( summer, winter )
	now = datetime.now(timezone)
	current_timestamp = datetime.timestamp(now)

	cprint(future_close_positions, 'white', 'on_red')
	for position in future_close_positions:
		if(position['symbol'] == selected_symbol):
			# cprint(selected_symbol, 'white', 'on_red')
			# cprint(str(position['timeToClose']) + '    ' + str(current_timestamp + 1), 'white', 'on_red')
			
			if(position['hasTrailingStopLoss'] == True):
				cprint('TRYING TO Modifying Trailing Stop Loss ' + str(selected_symbol), 'white', 'on_green')
				print(all_open_positions_from_market)
				# print(len(all_open_positions_from_market))
				# print(all_open_positions_from_market.iloc[0])

				# To update Trailing Stop Loss
				for live_pos_iter in range(len(all_open_positions_from_market)):
					live_pos_ticket = all_open_positions_from_market[live_pos_iter]['ticket']
					live_pos_profit = all_open_positions_from_market[live_pos_iter]['profit']
					previous_stop_loss = all_open_positions_from_market[live_pos_iter]['sl']

					if(live_pos_ticket == position['positionValue']):
						if(live_pos_profit > 0 or True):
							if(position['timeFrame'] > mt5.TIMEFRAME_M1 or True):
								cprint('position["timeFrame"] > mt5.TIMEFRAME_M1', 'white', 'on_green')
								cprint('Modifying Trailing Stop Loss', 'white', 'on_green')
								modifyTrailingStopLossTrade(position, live_pos_profit, previous_stop_loss)
						else:
							cprint('There is a Open position which is in LOSS with Ticket ID: ' + str(live_pos_ticket), 'white', 'on_red')

					else:
						cprint('There is a Open position with Ticket ID: ' + str(live_pos_ticket) + ' which is not recognised by Algo..', 'white', 'on_red')

	if(len(future_close_positions) > 0):
		cprint('REMAINING OPEN POSITIONS ARE :', 'red', 'on_yellow')
		cprint(future_close_positions, 'red', 'on_yellow')

