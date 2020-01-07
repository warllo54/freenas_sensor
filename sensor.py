from homeassistant.helpers.entity import Entity
import logging
import voluptuous as vol
import json
from freenas_api import FreeNASAPI
from homeassistant.components.sensor import PLATFORM_SCHEMA

from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_USERNAME,
    CONF_METHOD,
    CONF_NAME,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_PORT): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_METHOD): cv.string,
        vol.Required(CONF_NAME): cv.string,

    }
)

def setup_platform(hass, config, add_devices, discovery_info=None):

    """Setup the sensor platform."""


    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    user = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    method = config.get(CONF_METHOD)

    freenas_api = FreeNASAPI(method, host, port, user, password)

    dev = []
    dev.append(freenas_api)
    for freenas_api in dev:
        add_devices([FreeNasSensor(freenas_api, name)])

    


class FreeNasSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, freenas_api, name):
        """Initialize the sensor."""
        self._state = None
        self._data = None
        self._name = name
        self._client = freenas_api
        self._network_items = None
        self._network_item = None
        self._system_ready_items = None
        self._system_ready_item = None
        self._host_name = None
        

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        return {
            "Hostname" : self._host_name,
        }



    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._network_items = self._client.listnetworkconfig()
        self._network_item = json.loads(self._network_items)
        self._host_name = self._network_item['networkconfig']['hostname']
        self._system_ready_items = self._client.listsystemready()
        self._system_ready_item = json.loads(self._system_ready_items)
        if self._system_ready_item['systemready'] == True:
            self._state = 'Ready'
        elif self._system_ready_item['systemready'] == False:
            self._state = 'System Not Ready'
        elif self._system_ready_item['status'] != '200':
             self._state = 'Comm Error'
        else:
            _LOGGER.error("Failed to update sensor")


        return