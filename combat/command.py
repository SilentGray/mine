#----------------------------------------------------------------------------- 
# Module: Commands
#-----------------------------------------------------------------------------
"""Contains class information on unit commands"""

# Python imports.
import logging as log
import configparser
import random

# Module imports.
from utils.exceptions import CommandException
from utils.config import getBool
from display.interface import userInput

#------------------------------------------------------------------------------
# We support a number of potential action types.
#    'impact'     - Direct impact on a units health (damage or
#                   healing).
#    'boost'      - Direct impact on a units stat.
#------------------------------------------------------------------------------
IMPACT = 'impact'
BOOST = 'boost'

class Command:
    """Class for handling and manipulating unit commands"""

    def __init__(self, inputId):
        """Initialises a new command object"""
        log.debug('New Command Object, ID: %s' % inputId)

        self.commandId = inputId

        config = configparser.ConfigParser()
        config.read('custom/command.ini')

        if self.commandId not in config.sections():
            log.error('Invalid command ID: %s' % self.commandId)
            raise CommandException

        def getConfig(field):
            return config.get(self.commandId, field)

        self.name = getConfig('name')
        self.description = getConfig('description')

        self.actionType = getConfig('type')
        if self.actionType not in [IMPACT, BOOST]:
            log.error('Unrecognised action type: %s' % self.actionType)
            raise CommandException

        self.amount = int(getConfig('amount'))

        self.selfOnly = getBool(getConfig('self'))
        self.offensive = getBool(getConfig('offensive'))

        self.delay = int(getConfig('delay'))
        if self.delay:
            self.delayDescription = getConfig('delay_description')

        self.expiry = int(getConfig('expiry'))
        if self.expiry:
            self.expiryDescription = getConfig('expiry_description')

    def getTarget(self, targets, allies, auto=False):
        """Gets a target for an action"""
        log.debug('Getting a target')

        if auto:
            log.debug('Unit is automated')

            if self.offensive:
                return random.choice([unit for unit in targets
                                      if unit.team.name not in allies])
            else:
                return random.choice([unit for unit in targets
                                      if unit.team.name in allies])

        return userInput('Targets available for action:',
                         [act for act in (targets)])
