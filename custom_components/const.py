CONF_CLIENT = 'client'
CONF_PLATFORM = 'sensor'
CONF_GAS_TYPES = 'gasTypes'
CONF_GAS_COMPANIES = 'gas_companies'
DOMAIN = 'gasprices_dk'
DIESEL = 'diesel'
GAS_95 = '95'
GAS_COMPANIES = {
	'goon': {
		'name': 'Go\' on',
		'url': 'https://goon.nu/priser/#Aktuellelistepriser',
		'products': {GAS_95: 'Blyfri 95', DIESEL: 'Transportdiesel'}
	},
	'circlek': {
		'name': 'Circle K',
		'url': 'https://www.circlek.dk/',
		'products': {GAS_95: 'miles95', DIESEL: 'miles Diesel B7'}
	},
	'shell': {
		'name': 'Shell',
		'url': 'https://www.shell.dk/customer-service/priser-pa-benzin-og-diesel.html',
		'products': {GAS_95: 'Shell FuelSave Blyfri 95', DIESEL: 'Shell FuelSave Diesel'}
	},
	'ok': {
		'name': 'OK',
		'url': 'https://www.ok.dk/privat/produkter/priser',
		'products': {GAS_95: 'Blyfri 95', DIESEL: 'Diesel'},
	},
	'q8': {
		'name': 'Q8',
		'url': 'https://www.q8.dk/-/api/PriceViewProduct/GetPriceViewProducts',
		'headers': { 'Content-Type': 'application/json' },
		'payload': { 'FuelsIdList': [ { 'ProductCode': 22251 }, { 'ProductCode': 24451 } ] }
	},
	'f24': {
		'name': 'F24',
		'url': 'https://www.f24.dk/-/api/PriceViewProduct/GetPriceViewProducts',
		'headers': { 'Content-Type': 'application/json' },
		'payload': { 'FuelsIdList': [ { 'ProductCode': 22253 }, { 'ProductCode': 24453 } ] }
	},
	'oil': {
		'name': 'OIL! tank & go',
		'url': 'https://www.oil-tankstationer.dk/de-gaeldende-braendstofpriser/',
		'products': {GAS_95: '95 E10', DIESEL: 'Diesel'}
	},
	'ingo': {
		'name': 'ingo',
		'url': 'https://www.ingo.dk/br%C3%A6ndstofpriser/aktuelle-br%C3%A6ndstofpriser',
		'products': {GAS_95: 'Benzin 95', DIESEL: 'Diesel'}
	}
}
UPDATE_INTERVAL = 60

CREDITS = [
	{ 'Created by': 'J-Lindvig (https://github.com/J-Lindvig)' },
	{ 'Techinal support': 'www.fuelfinder.dk' }
]