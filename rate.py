import json
import requests
from datetime import datetime 
from credentials import API_KEY_EXCHANGE


#этот класс дает фактический курс обмена любой суммы из exchangeratesAPI
class ExchangeRate:
	def __init__(self):
		self.payload = {}
		self.headers= {
		  "apikey": f"{API_KEY_EXCHANGE}"
		}

	'''функция позволяет конвертировать валюту, она имеет три параметра: 
		первая сумма (должна быть int), это любая сумма, которую вы хотите конвертировать, 
		вторая (валюта, которую вы собираетесь изменить, например, рубли), 
		третья из (валюта, которой вы владеете, например, евро)
	'''
	def convert(self, amount, to, from_):
		try:
			self.url = f"https://api.apilayer.com/exchangerates_data/convert?to={to}&from={from_}&amount={amount}"
			self.response = requests.request("GET", self.url, headers=self.headers, data = self.payload)
			status_code = self.response.status_code
			self.result = json.loads(self.response.text)
			self.data = self.result['result']
			return f"{self.data:.2f}"
		except:
			pass
	
if __name__ == '__main__':
	ExchangeRate()

