#------------------------------------------------------------------------------
# Module: Config
#------------------------------------------------------------------------------
"""Module for providing additional config interfaces"""

# Module imports.
from utils.exceptions import ConfigException
import logging as log


def getBool(value):
    """Converts a config entry into a boolean"""
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    log.error('Expected \'true\' or \'false\', got \'%s\'' % value)
    raise ConfigException
