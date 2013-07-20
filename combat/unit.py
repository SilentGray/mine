#------------------------------------------------------------------------------
# Module: unit
#------------------------------------------------------------------------------
"""Contains class information on combat units"""

# Python imports
import logging as log
import configparser
import random

# Modules imports
from utils.exceptions import UnitException
from display.interface import userInput
import utils.counter as counter
import combat.command as command

# Status.
OK = 'OK'
DEAD = 'Dead'

class Unit:
    """Class for handling and manipulating combat units"""

    def __init__(self, inputId, auto=True):
        """Initialises a new combat unit"""
        log.debug('New Combat Unit, ID: %s' % inputId)

        self.unitId = inputId

        config = configparser.ConfigParser()
        config.read('custom/unit.ini')

        if self.unitId not in config.sections():
            log.error('Invalid unit ID: %s' % self.unitId)
            raise UnitException

        def getConfig(field):
            return config.get(self.unitId, field)

        self.name = getConfig('name')
        self.speed = int(getConfig('speed'))
        self.hitpoints = counter.Counter(int(getConfig('hitpoints')))

        # Whether the unit is automatic, or user-controlled.
        self.auto = auto

        # Setup a list of commands the unit can use.
        self._generate_commands(getConfig('commands').split(','))

    def _generate_commands(self, entries):
        """Generate the command objects for this unit"""
        log.debug('Adding commands to unit %s' % self)
        self.commands = []

        for entry in entries:
            newCommand = command.Command(entry)
            self.commands.append(newCommand)

    def turn(self, allies, hostiles):
        """Unit takes a turn"""
        log.debug('Turn from %s next' % self.name)

        choice = self.getChoice()
        targetChoice = self

        if not choice.selfOnly:
            log.debug('Prompting for a target')
            targetChoice = choice.getTarget(allies,
                                            hostiles,
                                            auto=self.auto)

        # Do action.

    def state(self):
        """Returns the state of the unit"""
        log.debug('Getting state for unit %s' % self.name)

        if self.hitpoints.value == 0:
            log.debug('Unit is dead')
            return DEAD

        return OK

    def canHeal(self):
        """Determines if unit is in a healable state"""
        result = (self.state() != DEAD)
        log.debug('Checking if can heal, result: %s' % result)
        return result

    def kill(self):
        """Kill a unit"""
        log.debug('Killing unit %s' % self.name)

        self.hitpoints.min()

    def reset(self):
        """Reset a unit"""
        log.debug('Resetting unit %s' % self.name)

        self.hitpoints.reset()

    def damage(self, amount):
        """Take set amount of damage"""
        log.debug('Unit %s takes %d damage' % (self.name, amount))

        self.hitpoints.reduce(amount)

    def damageFraction(self, fraction):
        """Take fractional damage"""
        log.debug('Unit %s takes %d fractional damage' % (self.name, fraction))

        self.hitpoints.reduceFraction(fraction)

    def heal(self, amount):
        """Heal a set amount"""
        log.debug('Unit %s heals %d' % (self.name, amount))

        if self.canHeal():
            self.hitpoints.increase(amount)

    def healFraction(self, fraction):
        """Heal a fractional amount"""
        log.debug('Unit %s heals by fraction %d' % (self.name, fraction))

        if self.canHeal():
            self.hitpoints.increaseFraction(fraction)

    def listCommands(self):
        """Returns commands available for a unit"""
        log.debug('Getting commands for %s' % self.name)
        return ', '.join([command.name for command in self.commands])

    def getChoice(self):
        """Gets an action for a turn"""
        log.debug('Getting an action')

        if self.auto:
            log.debug('Unit is automated')
            return random.choice(self.commands)

        return userInput('Commands available to %s:' % self.name,
                         [cmd for cmd in self.commands])
