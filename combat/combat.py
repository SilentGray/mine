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

# Unit info as printed in combat.
#   <Uniq-Id>: <HP>/<Max-HP>
#     <Full Name>
#     Status: <State>
UNITINFO = """%s %d/%d
-Unit    %s
-Status  %s"""


class Combat:
    """Class for managing, handling and displaying hostile combats"""

    def __init__(self, units):
        """Initialises a new combat"""
        log.debug('Initialise a new combat')

        self.units = units
        self._setupCombat()

    def _setupCombat(self):
        """Sets up the combat.

        This populates the active combat list and applies combat IDs to all
        of the units involved."""
        log.debug('Set up combat IDs')

        self.nextActive = 0
        names = {}

        self.combatList = []
        for entry in self.units:
            log.debug('Adding %s to combat-list.' % entry)

            if entry.uniqueName:
                log.debug('Use unique name "{0}"'.format(entry.uniqueName))
                idn = entry.uniqueName
            else:
                log.debug('Use non-unique ID "{0}"'.format(entry.unitId))
                idn = entry.unitId

            if idn in names:
                log.debug('Increment name {0}, previous usage: {1}'.format(idn, names[idn]))
                if entry.uniqueName:
                    log.error('Unique name already in use: "{0}"'.format(entry.uniqueName))
                names[idn] += 1
            else:
                log.debug('New name: {0}'.format(idn))
                names[idn] = 0

            if entry.uniqueName and names[idn] == 0:
                log.debug('Set unique name')
                entry.name = idn
            else:
                log.debug('Set non-unique name')
                entry.name = ''.join([idn, str(names[idn])])

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

            #------------------------------------------------------------------
            # Determine if a combat is finished.
            #------------------------------------------------------------------
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
            return(UNITINFO %
                   ('{:<8}'.format(entry.name),
                    entry.hitpoints.getValue(),
                    entry.hitpoints.maximum,
                    entry.longName,
                    entry.state()))

        def displayEntries(entries):
            maxNum = len(entries)
            for num in range(0, int(maxNum / 2)):
                intface.printTwoColumns(singleEntry(entries[num]),
                                        singleEntry(entries[num + 1]))
            if (maxNum % 2) is 1:
                intface.printTwoColumns(singleEntry(entries[maxNum - 1]),
                                        '')

        toDisplay = {}
        for unt in self.units:
            if unt.team.name not in toDisplay.keys():
                toDisplay[unt.team.name] = []

            toDisplay[unt.team.name].append(unt)

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
