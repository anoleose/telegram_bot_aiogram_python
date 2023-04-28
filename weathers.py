from credentials import API_KEY_WEATHER
import requests
import json 
from decimal import *

#этот класс выводит фактическую погоду в определяемом городе от OpenWeather API
class Weather:
	def __init__(self):
		self.API_KEY = API_KEY_WEATHER


	#этот метод конвертирует кельвины в градусы цельсия
	def convert_kelvin_to_celsius_fahrenheit(self, kelvin):
		celsius = kelvin - 273.15
		fahrenheit = celsius * (9/5) + 32
		return f"{celsius:.0f}"


	#метод получает температуру в градусах Цельсия в определенном городе
	def get_city_weather_temp(self, city):
		self.base_url = f"https://api.openweathermap.org/data/2.5/weather?"
		try:
			self.url = self.base_url + "appid=" + self.API_KEY +"&q=" + f"{city}"
			self.response = requests.get(self.url)
			self.status_code = self.response.status_code
			self.data = self.response.json()
			self.city = self.data['name']
			self.temp = self.data['main']['temp']
			self.celsius = self.convert_kelvin_to_celsius_fahrenheit(self.temp)
			return {'city':self.city, 'celsius':self.celsius}
		except:
			return False

if __name__ == '__main__':
	Weather()
	

