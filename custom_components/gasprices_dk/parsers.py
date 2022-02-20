import logging
import requests
import json
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta

class gasParser:
	def __init__(self, data_template = { '95' : {}, 'diesel': {}}):
		self._data_template = data_template
		self._session = requests.Session()

	def goon(self, params ):
		return self._getDataFromTD(params, 0, -1)

	def circlek(self, params ):
		return self._getDataFromTD(params, 1, -1)

	def shell(self, params ):
		return self._getDataFromTD(params, 0, -1)

	def ok(self, params):
		gasPrices = {}

		r = self._session.get(params['url'])
		html = BS(r.text, "html.parser")
		rows = html.find_all('div', {'role': 'row'})

		gasPrices.update(self._addCompanyAndTime(params['name']))
		for row in rows:
			cells = row.find_all('div', {'role': 'gridcell'})
			for key in self._data_template.keys():
				if cells:
					if key in params['products'].keys():
						if params['products'][key] == cells[0].text.strip():
							gasPrices.update(self._addProduct(key, cells[0].text, cells[1].text))
							params['products'].pop(key)
		return gasPrices

	def q8(self, params):
		return self._f24_q8(params)

	def f24(self, params):
		return self._f24_q8(params)

	def oil(self, params):
		gasPrices = {}

		r = self._session.get(params['url'])
		html = BS(r.text, "html.parser")
		rows = html.findAll('tr')
		spans = html.findAll('span', style=['text-align:right;', 'text-align:left;'])

		gasPrices.update(self._addCompanyAndTime(params['name']))
		firstIDx = 2
		for row in rows:
			cell = row.find('td')
			if cell:
				for key in self._data_template.keys():
					if key in params['products'].keys():
						if params['products'][key] == cell.text:
							gasPrices[key] = {'name': cell.text.strip()}
							# HARDCODING
							if len(params['products']) < 2:
								firstIDx = 10
							price = int(spans[firstIDx].text) + (int(spans[firstIDx + 1].text) / 100)
							gasPrices.update(self._addProduct(key, cell.text.strip(), price))
							params['products'].pop(key)
		return gasPrices

	def ingo(self, params):
		gasPrices = {}

		r = self._session.get(params['url'])
		html = BS(r.text, "html.parser")
		rows = html.findAll(class_ = ['views-field views-field-field-product-label', 'views-field views-field-price-gross'])

		gasPrices.update(self._addCompanyAndTime(params['name']))
		for i in range(len(rows)):
			for key in self._data_template.keys():
				if key in params['products'].keys():
					if params['products'][key] in rows[i].text.strip():
						gasPrices.update(self._addProduct(key, params['products'][key], rows[i + 1].text))
						params['products'].pop(key)
		return gasPrices

	def _f24_q8(self, params):
		gasPrices = {}

		now = datetime.now()
		fromDateTS = int((now - timedelta(days = 31)).timestamp())
		toDateTS = int(now.timestamp())
		params['payload']['FromDate'] = fromDateTS
		params['payload']['ToDate'] = toDateTS

		r = self._session.post(params['url'], headers = params['headers'], data = str(params['payload']))

		gasPrices.update(self._addCompanyAndTime(params['name'], toDateTS))
		for key in self._data_template.keys():
			gasPrices[key] = {}
			for product in r.json()['Products']:
				if key in product['Name'].lower():
					gasPrices.update(self._addProduct(key, product['Name'], product['PriceInclVATInclTax']))
		return gasPrices

	def _getDataFromTD(self, params, productIdx, priceIdx):
		gasPrices = {}

		r = self._session.get(params['url'])
		html = BS(r.text, "html.parser")
		rows = html.find_all('tr')

		gasPrices.update(self._addCompanyAndTime(params['name']))
		for row in rows:
			cells = row.findAll('td')
			for key in self._data_template.keys():
				if cells:
					if key in params['products'].keys():
						if params['products'][key] == cells[productIdx].text.strip():
							gasPrices.update(self._addProduct(key, cells[productIdx].text, cells[priceIdx].text))
							params['products'].pop(key)
		return gasPrices

	def _cleanPrice(self, price):
		price = str(price)
		price = price.strip()
		price = price.strip('Pris inkl. moms: ')
		price = price.strip(' kr.')
		price = price.replace(',', '.')
		return float("{:.2f}".format(float(price)))

	def _addCompanyAndTime(self, name, timestamp = None):
		if not timestamp:
			timestamp = int(datetime.now().timestamp())
		return {'name': name.strip(), 'lastUpdate': timestamp}

	def _addProduct(self, key, name, price):
		return {key: {'name': name.strip(), 'price': self._cleanPrice(price)}}
