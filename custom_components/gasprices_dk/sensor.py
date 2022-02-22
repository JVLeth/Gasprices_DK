from __future__ import annotations

import logging

from .const import (
	CREDITS,
	DIESEL,
	GAS_95,
	DOMAIN,
	CONF_CLIENT,
	CONF_PLATFORM,
	CONF_GAS_TYPES,
	CONF_GAS_COMPANIES,
	UPDATE_INTERVAL,
)
from homeassistant.const import DEVICE_CLASS_MONETARY, ATTR_ATTRIBUTION

from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER: logging.Logger = logging.getLogger(__package__)
_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info = None):
	"""Setup sensor platform"""

	async def async_update_data():
		# try:
		gasPrices = hass.data[DOMAIN][CONF_CLIENT]
		await hass.async_add_executor_job(gasPrices.getGasPrices)
		# except Exception as e:
		# 	raise UpdateFailed(f"Error communicating with server: {e}")

	coordinator = DataUpdateCoordinator(
		hass,
		_LOGGER,
		name = CONF_PLATFORM,
		update_method = async_update_data,
		update_interval = timedelta(minutes = UPDATE_INTERVAL)
	)

	# Immediate refresh
	await coordinator.async_request_refresh()

	# Add the sensors
	gasPrices = hass.data[DOMAIN][CONF_CLIENT]

	gasCompaniesFromConfig = hass.data[DOMAIN][CONF_GAS_COMPANIES]
	_LOGGER.debug("GASCOMPANIES: " + str(len(gasCompaniesFromConfig)))

	gasTypesFromConfig = hass.data[DOMAIN][CONF_GAS_TYPES]
	_LOGGER.debug("GASTYPES: " + str(len(gasTypesFromConfig)))
	
	entities = []
	gasCompanies = gasPrices.getGasCompanies()
	for name in gasCompanies:
		entities.append(GasPriceSensor(hass, coordinator, gasCompanies[name], DIESEL))
		entities.append(GasPriceSensor(hass, coordinator, gasCompanies[name], GAS_95))

	async_add_entities(entities)

class GasPriceSensor(SensorEntity):
	def __init__(self, hass, coordinator, gasCompany, gasType) -> None:
		self._hass = hass
		self._coordinator = coordinator
		self._gasType = gasType
		self._companyName = gasCompany['name']
		self._productName = gasCompany[gasType]['name']
		self._company_logo = gasCompany['company_logo']
		self._lastUpdate = gasCompany['lastUpdate']

		self._name = gasCompany['name'] + ' ' + gasType
		self._state = gasCompany[gasType]['price']
		self._icon = 'mdi:gas-station'

	@property
	def name(self) -> str:
		return self._name

	@property
	def state(self):
		return self._state

	@property
	def extra_state_attributes(self):
		# Prepare a dictionary with a list of credits
		attr = {}
		
		attr['company_name'] = self._companyName
		attr['company_logo'] = self._company_logo
		attr['product_name'] = self._productName
		attr['last_update'] = self._lastUpdate

		attr[ATTR_ATTRIBUTION] = CREDITS

		return attr

	@property
	def icon(self):
		return self._icon

	@property
	def unique_id(self):
		return self._name + '_' + self._gasType

	@property
	def device_class(self) -> str:
		return DEVICE_CLASS_MONETARY

	@property
	def should_poll(self):
		"""No need to poll. Coordinator notifies entity of updates."""
		return False

	@property
	def available(self):
		"""Return if entity is available."""
		return self._coordinator.last_update_success

	async def async_update(self):
		"""Update the entity. Only used by the generic entity update service."""
		await self._coordinator.async_request_refresh()

	async def async_added_to_hass(self):
		"""When entity is added to hass."""
		self.async_on_remove(
			self._coordinator.async_add_listener(
				self.async_write_ha_state
			)
		)