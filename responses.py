#coding:utf-8

from weathers import Weather
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


#эта функция содержит все ответы о погоде в указанном городе.
city_list = []
def weather_responses(enter_message):
	if "/weather" in enter_message:
		city_list.append(enter_message)
		return "какой город"
	if len(city_list) > 0:
		try:
			data = Weather().get_city_weather_temp(enter_message)
			city = data['city']
			temp = data['celsius']
			city_list.clear()
			return f"{city} {temp} °C \n /weather найти другой город"
		except:
			pass



#эта функция содержит все ответы об обменном курсе USD/RUB RUB/USD EUR/RUB RUB/EUR
rate_list = []
def rate_responses(enter_message):
	if "/rate" in enter_message:
		rate_list.append(enter_message)
		return "Пожалуйста, введите сумму"
	if len(rate_list) > 0:
		amount = int(enter_message.strip())
		if amount > 0:
			keyboard = [
				[
					InlineKeyboardButton(f"USD/RUB", callback_data = 'usd/rub'),
					InlineKeyboardButton(f"RUB/USD", callback_data="rub/usd"),
					
				],
				[
					InlineKeyboardButton(f"EUR/RUB", callback_data = 'eur/rub'),
					InlineKeyboardButton(f"RUB/EUR", callback_data="rub/eur"),
					
				],
			]

			reply_markup = InlineKeyboardMarkup(row_width=2, inline_keyboard=keyboard)
			rate_list.clear()
			return [amount, reply_markup]
	else:
		pass



#эта функция содержит все ответы об опросе
poll_list = []
start_list = []
def poll_responses(enter_message):
	if enter_message == "/poll":
		start_list.append(enter_message)
		poll_list.clear()
		return "Создайте новый опрос, отправьте сначала свой вопрос"

	if "/poll" in start_list:
		if enter_message != "/done":
			poll_list.append(enter_message)

		if len(poll_list) == 0:
			if enter_message == "/done": 
				return "Пожалуйста, пришлите хотя бы один вопрос и несколько вариантов"

		elif len(poll_list) == 1:
			if enter_message == "/done": 
				return "пришлите хотя бы 2 варианта"
			else:
				return f"Вопрос:{enter_message}\n Пожалуйста, пришлите варианты."
			
		elif len(poll_list) > 1:
			if enter_message == "/done":
				question = poll_list[0]
				options = poll_list[1:]
				return [question, options, poll_list.clear(), start_list.clear()]
			else:
				return f"Добавьте еще раз новую опцию, отправить /done чтобы опубликовать свой опрос"
		else:
			pass
	elif "/done" in enter_message:
		return "/poll -создать новый опрос"
	else:
		pass

	





