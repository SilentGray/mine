#------------------------------------------------------------------------------
# Module: combat.py
#------------------------------------------------------------------------------
"""Module for managing a combat"""

# Python imports.
import logging as log

# Module imports.
from utils.exceptions import CombatException
import combat.timer as timer
import combat.unit as unit
import display.interface as intface

# Combat results.
LOSS = 1
VICTORY = 2

class Combat:
    """Class for managing, handling and displaying hostile combats"""

    def __init__(self, units, hostiles):
        """Initialises a new combat"""
        log.debug('Initialise a new combat')

        self.units = units
        self.hostiles = hostiles
        self.nextActive = 0

        self.combatList = []
        for entry in self.units + self.hostiles:
            log.debug('Adding %s to combat-list.' % entry)
            self.combatList.append(timer.Timer(entry,
                                               entry.speed,
                                               recurring=True))

    def run(self):
        """Runs a combat"""
        log.info('Running commbat')

        while (len(self.units) > 0) and (len(self.hostiles) > 0):
            nextEvent = self.spin()
            log.debug('Next event: %s' % nextEvent)

            intface.printSpacer()
            intface.printBlank()
            self.printStatus()
            intface.printBlank()
            intface.printSpacer()

            #------------------------------------------------------------------
            # For units we let them handle an action.
            #------------------------------------------------------------------
            if isinstance(nextEvent.subject, unit.Unit):
                log.debug('Next event is a unit')
                if nextEvent.subject in self.units:
                    log.debug('Next event is a friendly unit')
                    nextEvent.subject.turn(self.units,
                                           self.hostiles)
                elif nextEvent.subject in self.hostiles:
                    log.debug('Next event is a hostile unit')
                    nextEvent.subject.turn(self.units,
                                           self.hostiles,
                                           user=True)
                else:
                    log.error('Unrecognised unit found in combat')
                    log.debug('Unit: %s - %s' % (nextEvent.subject.name,
                                                 nextEvent.subject))
                    raise CombatException

            #------------------------------------------------------------------
            # For events trigger the event action.
            #------------------------------------------------------------------
            else:
                log.debug('Next event is not a unit')
                raise CombatException
                # General event handling not yet implemented

        #----------------------------------------------------------------------
        # Determine if a combat is finished.
        #----------------------------------------------------------------------
        if len(self.units) is 0:
            return LOSS
        elif len(self.hostiles is 0):
            return VICTORY

    def spin(self):
        """Cycle the combat to the next action"""
        log.debug('Spinning cycle')
        cycles = 0

        #----------------------------------------------------------------------
        # For safety ensure we find a result within 500 cycles.
        #----------------------------------------------------------------------
        while cycles < 500:
            for event in (self.combatList[self.nextActive:] +
                          self.combatList[:self.nextActive]):
                log.debug('Checking %s' % event)
                result = event.checkValid()

                if result is not timer.SILENT:
                    log.debug('Found next event: %s' % event)
                    if result is timer.POP_DIE:
                        self.combatList.remove(event)
                    self.nextActive = self.combatList.index(event) + 1

                    if self.nextActive > len(self.combatList):
                        self.nextActive = 0
                    return event

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
            return("""%s: %d/%d\n  Status: OK""" %
                                                  ('{:<15}'.format(entry.name),
                                                   entry.hitpoints.getValue(),
                                                   entry.hitpoints.maximum))

        def displayEntries(entries):
            maxNum = len(entries)
            for num in range(0, int(maxNum/2)):
                intface.printTwoColumns(singleEntry(entries[num]),
                                        singleEntry(entries[num + 1]))
            if (maxNum % 2) is 1:
                intface.printTwoColumns(singleEntry(entries[maxNum - 1]),
                                        '')

        displayEntries(self.units)
        intface.printBlank()
        displayEntries(self.hostiles)

    def printCommands(self, unit):
        """Prints commands available for the next turn"""
        log.debug('Printing commands for %s' % unit.name)

        intface.printText('Available actions for %s:' % unit.name)
        intface.printText('  %s' % unit.listCommands())

    def printAction(self, command, target):
        """Prints an action"""
        log.debug('Printing a combat action')

        pass
