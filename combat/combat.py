#------------------------------------------------------------------------------
# Module: combat.py
#------------------------------------------------------------------------------
"""Module for managing a combat"""

# Python imports.
import logging as log

# Module imports.
from utils.exceptions import CombatException
import combat.event as event
import combat.unit as unit
import display.interface as intface

# Combat results.
LOSS = 1
VICTORY = 2

LIST_LIMIT = 4

class Combat:
    """Class for managing, handling and displaying hostile combats"""

    def __init__(self, units):
        """Initialises a new combat"""
        log.debug('Initialise a new combat')

        self.units = units
        self.nextActive = 0

        self.combatList = []
        for entry in self.units:
            log.debug('Adding %s to combat-list.' % entry)
            self.combatList.append(entry)

    def run(self):
        """Runs a combat"""
        log.info('Running commbat')

        while (len(self.units) > 0):
            nextEvent = self.spin()
            log.debug('Next event: %s' % nextEvent)

            intface.printRefresh()
            intface.printSpacer()
            intface.printBlank()
            self.printStatus()
            self.printOrder()
            intface.printBlank()
            intface.printSpacer()

            nextEvent.turn(self.units)

            #----------------------------------------------------------------------
            # Determine if a combat is finished.
            #----------------------------------------------------------------------
            if len(self.units) is 0:
                return LOSS

        #----------------------------------------------------------------------
        # Unexpected exit of run function.
        #----------------------------------------------------------------------
        raise CombatException('Unexpected exit of running combat')

    def activelist(self):
        """Returns the active combatlist"""
        return (self.combatList[self.nextActive:] +
                self.combatList[:self.nextActive])

    def spin(self):
        """Cycle the combat to the next action"""
        log.debug('Spinning cycle')
        cycles = 0

        #----------------------------------------------------------------------
        # For safety ensure we find a result within 500 cycles.
        #----------------------------------------------------------------------
        while cycles < 500:
            for action in self.activelist():
                log.debug('Checking %s' % event)
                result = action.checkValid()

                if result is not event.SILENT:
                    log.debug('Found next event: %s' % action)
                    if result is event.POP_DIE:
                        self.combatList.remove(action)
                    self.nextActive = self.combatList.index(action) + 1

                    if self.nextActive > len(self.combatList):
                        self.nextActive = 0
                    return action

            cycles += 1
        log.error('Cycle span for too long without a result')
        raise CombatException

    #--------------------------------------------------------------------------
    # Combat display handling.
    #--------------------------------------------------------------------------
    def printStatus(self):
        """Prints the combat status display"""
        log.debug('Printing combat status')

        def singleEntry(entry):
            return("""%s: %d/%d\n  Status: %s""" %
                                                  ('{:<15}'.format(entry.name),
                                                   entry.hitpoints.getValue(),
                                                   entry.hitpoints.maximum,
                                                   entry.state()))

        def displayEntries(entries):
            maxNum = len(entries)
            for num in range(0, int(maxNum/2)):
                intface.printTwoColumns(singleEntry(entries[num]),
                                        singleEntry(entries[num + 1]))
            if (maxNum % 2) is 1:
                intface.printTwoColumns(singleEntry(entries[maxNum - 1]),
                                        '')

        toDisplay = {}
        for unit in self.units:
            if unit.team.name not in toDisplay.keys():
                toDisplay[unit.team.name] = []

            toDisplay[unit.team.name].append(unit)

        for team in toDisplay.keys():
            intface.printText('-- %s --' % team)
            displayEntries(toDisplay[team])
            intface.printBlank()

    def printOrder(self):
        """Prints the upcoming combat order"""
        log.debug('Printing combat order')

        numToPrint = len([un for un in self.units if un.state() != unit.DEAD])
        if numToPrint > LIST_LIMIT:
            log.debug('Limit combat list to next four units')
            numToPrint = LIST_LIMIT

        if numToPrint > len(self.activelist()):
            raise CombatException

        intface.printText('Upcoming turns:')
        intface.printText('  ' + ', '.join([entry.name for entry in
                                            self.activelist()[:numToPrint]]))

    def printCommands(self, unit):
        """Prints commands available for the next turn"""
        log.debug('Printing commands for %s' % unit.name)

        intface.printText('Available actions for %s:' % unit.name)
        intface.printText('  %s' % unit.listCommands())
