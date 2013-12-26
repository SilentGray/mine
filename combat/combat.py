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

# Victory conditions.
DEATHMATCH = 0

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

    def __init__(self, units, victory=DEATHMATCH):
        """Initialises a new combat"""
        log.debug('Initialise a new combat')

        self.units = units
        self._setVictoryCond(victory)
        self._setupCombat()

    def _setVictoryCond(self, victoryCondId):
        """Sets the victory condition for the combat"""
        log.debug('Set victory condition')

        victoryCond = {DEATHMATCH: self.conditionDeathmatch}

        self.checkCombatEnd = victoryCond[victoryCondId]

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
                log.debug('Increment name {0}, previous usage: {1}'.format(
                          idn, names[idn]))
                if entry.uniqueName:
                    log.error('Unique name already in use: "{0}"'.format(
                              entry.uniqueName))
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

    def _cleanUnits(self):
        """Remove dead units from the combatlist"""
        log.debug('Removing dead units')

        for unt in self.combatList:
            log.debug('Check unit: {0}'.format(unt))
            if unt.state() == unit.DEAD:
                log.info('Remove dead unit: {0}'.format(unt.name))
                self.combatList.remove(unt)

    def run(self):
        """Runs a combat"""
        log.info('Running combat')

        if not self.checkCombatEnd:
            log.error('No combat end conditions set')
            raise CombatException('No combat end conditions set')

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
            self._cleanUnits()

            victors = self.checkCombatEnd()
            if victors != None:
                log.debug('Combat finished, outcome {0}'.format(', '.join(victors)))
                return victors

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
    # Combat end conditions.
    #
    # These return either 'None' (no winner - yet), or by returning a
    # list of the winning team IDs.
    #--------------------------------------------------------------------------
    def conditionDeathmatch(self):
        """Traditional match to the death.

        Victory occurs when all teams have removed their oppositions.

        """
        log.debug('Checking condition "Deathmatch"')

        liveTeams = {}
        matchFin = True

        for unt in self.units:
            log.debug('Checking unit {0}'.format(unt))
            if unt.state() != unit.DEAD and unt.team.teamId not in liveTeams:
                log.debug('Add new live team: {0}'.format(unt.team.teamId))
                liveTeams[unt.team.teamId] = unt.team.allies

        log.debug('Live teams: {0}'.format(', '.join(liveTeams.keys())))

        for team, allies in liveTeams.items():
            log.debug('Check team {0} with allies: {1}'.format(team,
                      ', '.join(allies)))

            for otherTeam in liveTeams.keys():
                log.debug('Check team {0}'.format(otherTeam))
                if otherTeam not in allies:
                    log.debug('Enemy team still standing')
                    matchFin = False

        if matchFin:
            log.debug('Battle finished')
            return [tm for tm in liveTeams.keys()]
        else:
            log.debug('Battle incomplete')
            return None

    #--------------------------------------------------------------------------
    # Combat display handling.
    #--------------------------------------------------------------------------
    def printStatus(self):
        """Prints the combat status display"""
        log.debug('Printing combat status')

        def singleEntry(entry):
            return(UNITINFO %
                   ('{:<8}'.format(entry.name),
                    entry.attributes[unit.HP].value,
                    entry.attributes[unit.HP].maximum,
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
            if unt.team.longName not in toDisplay.keys():
                toDisplay[unt.team.longName] = []

            toDisplay[unt.team.longName].append(unt)

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
