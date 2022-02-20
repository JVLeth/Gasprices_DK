from __future__ import annotations

import logging

from .gasprices_dk import gasprices_dk_api

from .const import (
	DOMAIN,
	CONF_CLIENT,
	CONF_PLATFORM,
	CONF_GAS_TYPES,
	CONF_GAS_COMPANIES,
	)

_LOGGER: logging.Logger = logging.getLogger(__package__)
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
	conf = config.get(DOMAIN)
	if conf is None:
		return True

	# Get custom events and the flags in inventory from the config
	gasTypes = config[DOMAIN].get('gas_types', {})
	_LOGGER.debug("gas_types loaded from config: " + str(len(gasTypes)))
	gasCompanies = config[DOMAIN].get('gas_companies', {})
	_LOGGER.debug("gas_companies loaded from config: " + str(len(gasCompanies)))

	# Initialize the Client
	client  = gasprices_dk_api()
	hass.data[DOMAIN] = {
		CONF_CLIENT: client,
		CONF_GAS_TYPES: gasTypes,
		CONF_GAS_COMPANIES: gasCompanies,
	}

	# Add sensors
	hass.async_create_task(
		hass.helpers.discovery.async_load_platform(CONF_PLATFORM, DOMAIN, conf, config)
	)

	# Initialization was successful.
	return True