#------------------------------------------------------------------------------
# Module: unit
#------------------------------------------------------------------------------
"""Contains class information on combat units"""

# Python imports
import logging as log
import configparser

# Modules imports
import utils.counter as counter

class Unit:
    """Class for handling and manipulating combat units"""

    def __init__(self, inputId):
        """Initialises a new combat unit"""
        log.debug('New Combat Unit, ID: %s' % inputId)

        self.unitId = inputId

        config = configparser.ConfigParser()
        config.read('custom/unit.ini')

        if self.unitID not in config.sections():
            log.error('Invalid unit ID: %s' % self.unitId)
            raise Exception

        self.name = config.get(self.unitId, 'name')
        self.hitpoints = counter.Counter(config.get(self.unitId, 'hitpoints'))

    def kill(self):
        """Kill a unit"""
        log.debug('Killing unit %s' % self.name)

        self.hitpoints.min()

    def reset(self):
        """Reset a unit"""
        log.debug('Resetting unit %s' % self.name)

        self.hitpoints.reset()
