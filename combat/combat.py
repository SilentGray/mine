#------------------------------------------------------------------------------
# Module: combat.py
#------------------------------------------------------------------------------
"""Module for managing a combat"""

# Python imports.
import logging as log

# Module imports.

class Combat:
    """Class for managing, handling and displaying hostile combats"""

    def __init__(self, units, hostiles):
        """Initialises a new combat"""
        log.debug('Initialise a new combat')

        self.units = units
        self.hostiles = hostiles
        self.nextActive = 0

        self.combatList = []
        for entries in [self.units, self.hostiles]:
            for entry in entries:
                log.debug('Adding %s to combat-list.' % entry)
                self.combatList.append(entry)

    def spin(self):
        """Cycle the combat to the next action"""
        log.debug('Spinning cycle')
        cycles = 0

        #----------------------------------------------------------------------
        # For safety ensure we find a result within 500 cycles.
        #----------------------------------------------------------------------
        while cycles < 500:
            for unit in (self.combatList[self.nextActive:] +
                         self.combatList[:self.nextActive]):
                log.debug('Checking %s' % unit)

                unit.speedCount.reduce(1)
                if unit.speedCount.getValue() is 0:
                    log.debug('Found next unit to act: %s' % unit)
                    unit.speedCount.reset()
                    self.nextActive = self.combatList.index(unit) + 1

                    if self.nextActive > len(self.combatList):
                        self.nextActive = 0
                    return unit

            cycles += 1

        raise Exception

    def printStatus(self):
        pass

    def printCommands(self):
        pass
