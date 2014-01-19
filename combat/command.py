#-----------------------------------------------------------------------------
# Module: Command
#-----------------------------------------------------------------------------
"""Contains class information on unit commands"""

# Python imports.
import logging as log
import configparser
import random

# Module imports.
from utils.exceptions import CommandException
from utils.config import getBool
from combat.action import Action
from display.interface import userInput


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

        self.name = self.commandId
        self.description = getConfig('description')

        self.selfOnly = getBool(getConfig('self'))
        self.offensive = getBool(getConfig('offensive'))

        self.amount = int(getConfig('amount'))
        self.actionType = getConfig('type')

        rawAttrs = getConfig('buffattr').split(',')
        self.buffAttrs = [attr.strip() for attr in rawAttrs
                          if attr.strip() is not '']

        self.delay = int(getConfig('delay'))
        if self.delay:
            log.debug('Delayed action')
            self.delayDescription = getConfig('delay_description')

        self.expiry = int(getConfig('expiry'))
        if self.expiry:
            self.expiryDescription = getConfig('expiry_description')

    def getTarget(self, targets, allies, auto=False):
        """Gets a target for an action"""
        log.debug('Getting a target, excluding allies: {0}'.format(
                  ', '.join(allies)))

        if auto:
            log.debug('Unit is automated')

            if self.offensive:
                log.debug('Offensive attack')
                validTargets = [unit for unit in targets
                                if unit.team.name not in allies]
            else:
                log.debug('Non-offensive attack')
                validTargets = [unit for unit in targets
                                if unit.team.name in allies]

            log.debug('Choice of target from: {0}'.format(', '.join(
                      [unit.name for unit in validTargets])))
            return random.choice(validTargets)

        return userInput('Targets available for action:',
                         [act for act in (targets)])

    def activate(self, caller, target):
        """Performs the command.

        This will create an appropriate action and then may run it and/or
        return the action as an event for the combat to activate later.

        """
        log.debug('Activating command: {0}'.format(self.name))

        newAction = Action(self, caller, target)

        if newAction.event:
            log.debug('Action has prepared an event.')
            return newAction
