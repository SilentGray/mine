#------------------------------------------------------------------------------
# Module: combat.py
#------------------------------------------------------------------------------
"""Module for managing a combat"""

# Python imports.
import logging as log

# Module imports.
import combat.timer as timer
import display.interface as intface

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
                    return event.subject

            cycles += 1
        raise Exception

    def printStatus(self):
        """Prints the combat status display"""
        log.debug('Printing combat status')

        intface.printSpacer()
        intface.printBlank()

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

        intface.printBlank()

    def printCommands(self, unit):
        """Prints commands available for the next turn"""
        log.debug('Printing commands for %s' % unit.name)

        intface.printSpacer()
        intface.printText('Available actions for %s:' % unit.name)
        intface.printText('  %s' % unit.listCommands())
        intface.printSpacer()
