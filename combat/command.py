#----------------------------------------------------------------------------- 
# Module: Commands
#-----------------------------------------------------------------------------
"""Contains class information on unit commands"""

# Python imports.
import logging as log
import configparser

# Action-types.
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
            raise Exception

        def getConfig(field):
            return config.get(self.commandId, field)

        self.name = getConfig('name')
        self.description = getConfig('description')

        #----------------------------------------------------------------------
        # We support a number of potential action types.
        #    'impact'     - Direct impact on a units health (damage or 
        #                   healing).
        #    'boost'      - Direct impact on a units stat.
        #---------------------------------------------------------------------- 
        self.actionType = getConfig('type')
        if self.actionType not in [IMPACT, BOOST]:
            log.error('Unrecognised action type: %s' % self.actionType)
            raise Exception

        self.amount = int(getConfig('amount'))

        selfOnly = getConfig('self')
        if selfOnly.lower == 'true':
            self.selfOnly = True
        else:
            self.selfOnly = False

        self.delay = int(getConfig('delay'))
        if self.delay:
            self.delayDescription = getConfig('delay_description')

        self.expiry = int(getConfig('expiry'))
        if self.expiry:
            self.expiryDescription = getConfig('expiry_description')
