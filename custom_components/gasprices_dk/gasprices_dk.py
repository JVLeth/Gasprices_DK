from __future__ import annotations

import logging
import requests                     # Perform http/https requests
from bs4 import BeautifulSoup as BS # Parse HTML pages
import json                         # Needed to print JSON API data
from datetime import datetime
from .parsers import gasParser

from .const import (
	DIESEL,
	GAS_95,
	GAS_COMPANIES,
)

class gasprices_dk_api:
	def __init__(self):
		self._session = None
		self._gasPrices = {}
		self._parser = gasParser()

	def getGasCompanies(self):
		return self._gasPrices

	def getGasPrices(self):
		for company in GAS_COMPANIES.keys():
			self._gasPrices[company] = getattr(self._parser, company)(GAS_COMPANIES[company])

	def _getDiscount(self):
		for company in GAS_COMPANIES.keys():
			if 'discount' in GAS_COMPANIES[company].keys():
				print('Before: ' + str(self._gasPrices[company][GAS_95]['price']))
				self._gasPrices[company][GAS_95]['price'] = float("{:.2f}".format(self._gasPrices[company][GAS_95]['price'] - GAS_COMPANIES[company]['discount']))
				print('After: ' + str(self._gasPrices[company][GAS_95]['price']))