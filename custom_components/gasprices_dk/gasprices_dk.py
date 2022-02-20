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
