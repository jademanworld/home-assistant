"""
homeassistant.components.ifttt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This component enable you to trigger Maker IFTTT recipes.
Check https://ifttt.com/maker for details.

Configuration:

To use Maker IFTTT you will need to add something like the following to your
config/configuration.yaml.

ifttt:
  key: xxxxx-x-xxxxxxxxxxxxx

Variables:

key
*Required
Your api key

"""
import logging
import requests

from homeassistant.helpers import validate_config

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ifttt"

SERVICE_TRIGGER = 'trigger'

ATTR_EVENT = 'event'
ATTR_VALUE1 = 'value1'
ATTR_VALUE2 = 'value2'
ATTR_VALUE3 = 'value3'

DEPENDENCIES = []

REQUIREMENTS = ['pyfttt==0.3']


def trigger(hass, event, value1=None, value2=None, value3=None):
    """ Trigger a Maker IFTTT recipe """
    data = {
        ATTR_EVENT: event,
        ATTR_VALUE1: value1,
        ATTR_VALUE2: value2,
        ATTR_VALUE3: value3,
    }
    hass.services.call(DOMAIN, SERVICE_TRIGGER, data)


def setup(hass, config):
    """ Setup the ifttt service component """

    if not validate_config(config, {DOMAIN: ['key']}, _LOGGER):
        return False

    key = config[DOMAIN]['key']

    def trigger_service(call):
        """ Handle ifttt trigger service calls. """
        event = call.data.get(ATTR_EVENT)
        value1 = call.data.get(ATTR_VALUE1)
        value2 = call.data.get(ATTR_VALUE2)
        value3 = call.data.get(ATTR_VALUE3)
        if event is None:
            return

        try:
            import pyfttt as pyfttt
            pyfttt.send_event(key, event, value1, value2, value3)
        except requests.exceptions.RequestException:
            _LOGGER.exception("Error communicating with IFTTT")

    hass.services.register(DOMAIN, SERVICE_TRIGGER, trigger_service)

    return True
