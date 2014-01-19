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
import combat.event as event
import combat.action as action
import combat.command as command
import combat.team as team

# Status.
OK = 'OK'
DEAD = 'Dead'

# Attribute definitions
HP = 'hitpoints'
DEF = 'defence'
EVA = 'evasion'
SPE = 'speed'
ATT = 'attack'

# Maximum stat for non-HP attributes
MAXSTAT = 100

# Attribute categories
SIMATTR = [DEF, EVA, SPE]


class Unit(event.Event):
    """Class for handling and manipulating combat units"""

    def __init__(self, inputId, unitTeam, auto=True):
        """Initialises a new combat unit"""
        log.debug('New Combat Unit, ID: %s' % inputId)

        self.unitId = inputId
        if not unitTeam:
            raise UnitException('Unit %s initialised without team' % inputId)

        config = None

        def getConfig(field):
            """Get a value from the current config file"""
            return config.get(self.unitId, field)

        unitfile = 'custom/unit.ini'
        config = configparser.ConfigParser()
        config.read(unitfile)
        if self.unitId not in config.sections():
            raise UnitException('Invalid value; key \'%s\' not in %s' %
                                (self.unitId, unitfile))

        # Name usage:
        # .name       - short-term name storage, preserved for length of a
        #               combat
        # .uniqueName - permanant storage of a unique name
        # .longName   - permanant storage of a full unit-type name
        self.name = None
        self.uniqueName = None
        self.longName = getConfig('name')

        self.team = team.Team(unitTeam)

        # Attribute intitialization
        self._setupAttr(getConfig)

        # Event initialisation.
        event.Event.__init__(self,
                             self.attributes[SPE].value,
                             recurring=True)

        # Whether the unit is automatic, or user-controlled.
        self.auto = auto

        # Setup a list of commands the unit can use.
        self._generate_commands(getConfig('commands').split(','))

    def _setupAttr(self, configGetter):
        """Sets the default attributes for the unit, as outlaid in the config
        file.

        """
        log.debug('Setting default attributes')

        self.attributes = {}

        def setStat(value):
            """Returns a counter for a single stat.

            Sets up a new counter up to _MAXSTAT_ at the value given.

            """
            log.debug('Setting stat')
            stat = counter.Counter(MAXSTAT)
            stat.default = value
            stat.reset()
            return stat

        # Setup HP, which does not obey _MAXSTAT_.
        self.attributes[HP] = counter.Counter(int(configGetter(HP)))

        # Setup simple attributes
        for attr in SIMATTR:
            log.debug('Setup attribute: {0}'.format(attr))
            self.attributes[attr] = setStat(int(configGetter(attr)))

        # Setup all the attack attributes
        self.attributes[ATT] = {}
        for attattr in action.ATTACKTYPES:
            log.debug('Setup attack attribute: {0}'.format(attr))
            self.attributes[ATT][attattr] = setStat(int(configGetter(attattr)))

    def _generate_commands(self, entries):
        """Generate the command objects for this unit"""
        log.debug('Adding commands to unit %s' % self)
        self.commands = []

        self.commands.append(command.Command('attack'))

        for entry in entries:

            # Ignore blank string commands
            if entry:
                newCommand = command.Command(entry)
                self.commands.append(newCommand)

        self.commands.append(command.Command('pass'))

    def getAttack(self, attType):
        """Returns the value of the attack stat _type_."""
        return self.attributes[ATT][attType].value

    def getDefence(self):
        """Returns the value of the defence stat."""
        return self.attributes[DEF].value

    def setName(self, name):
        """Sets a unique name for a unit."""
        log.debug('Setting unique name {0}'.format(name))
        self.uniqueName = name

    def turn(self, targets):
        """Unit takes a turn

        This will return an event to add to the combatlist if required.

        """
        log.debug('Turn from %s next' % self.name)

        choice = self.getChoice()
        targetChoice = self

        if not choice.selfOnly:
            log.debug('Prompting for a target')
            targetChoice = choice.getTarget(targets,
                                            self.team.allies,
                                            auto=self.auto)

        # Do action.
        log.debug('%s uses %s on %s' % (self.name,
                                        choice.name,
                                        targetChoice.name))
        return choice.activate(self, targetChoice)

    def state(self):
        """Returns the state of the unit"""
        log.debug('Getting state for unit %s' % self.name)

        if self.attributes[HP].value == 0:
            log.debug('Unit is dead')
            return DEAD

        return OK

    def canHeal(self):
        """Determines if unit is in a healable state"""
        result = (self.state() != DEAD)
        log.debug('Checking if can heal, result: %s' % result)
        return result

    def canDamage(self):
        """Determines if unit can be damaged"""
        result = (self.state() != DEAD)
        log.debug('Checking if can damage, result: %s' % result)
        return result

    def kill(self):
        """Kill a unit"""
        log.debug('Killing unit %s' % self.name)

        self.attributes[HP].min()

    def reset(self):
        """Reset a unit"""
        log.debug('Resetting unit %s' % self.name)

        log.debug('Reset {0}'.format(HP))
        self.attributes[HP].reset()

        for attr in SIMATTR:
            log.debug('Reset {0}'.format(attr))
            self.attributes[attr].reset()

        for attAttr in action.ATTACKTYPES:
            log.debug('Reset attack-{0}'.format(attAttr))
            self.attributes[ATT][attAttr].reset()

    def buff(self, attr, amount):
        """Buff attribute _attr_ by _amount_

        Returns the actual change in the attribute.

        """
        log.debug('Buffing {0} by {1}'.format(attr, amount))

        if attr in action.ATTACKTYPES:
            log.debug('Attribute is an attack type')
            attrLoc = self.attributes[ATT][attr]
        elif attr == ATT:
            log.debug('Attribute is the general attack stat')
            raise UnitException('Attempt to buff the general attack stat; '
                                'which is unsupported')
        else:
            log.debug('Attribute is a base type')
            attrLoc = self.attributes[attr]

        return attrLoc.increase(amount)

    def damage(self, amount):
        """Take set amount of damage"""
        log.debug('Unit %s takes %d damage' % (self.name, amount))

        if self.canDamage():
            self.attributes[HP].reduce(amount)

    def damageFraction(self, fraction):
        """Take fractional damage"""
        log.debug('Unit %s takes %d fractional damage' % (self.name, fraction))

        if self.canDamage():
            self.attributes[HP].reduceFraction(fraction)

    def heal(self, amount):
        """Heal a set amount"""
        log.debug('Unit %s heals %d' % (self.name, amount))

        if self.canHeal():
            self.attributes[HP].increase(amount)

    def healFraction(self, fraction):
        """Heal a fractional amount"""
        log.debug('Unit %s heals by fraction %d' % (self.name, fraction))

        if self.canHeal():
            self.attributes[HP].increaseFraction(fraction)

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
