#-----------------------------------------------------------------------------
# Script: combattests
#-----------------------------------------------------------------------------
"""Unittest script for combat functions"""

# Python imports.
import logging as log
import unittest
import sys

sys.path.append('.')

# Module imports.
import combat.action as action
import combat.combat as combat
import combat.unit as unit
import combat.command as command
import combat.event as event
import combat.team as team
import utils.exceptions as exceptions
import unittests.testutils.testutils as testutils

log.basicConfig(filename='logs/combattests.log',
                level=log.DEBUG,
                filemode='w',
                format='%(levelname)s >> %(message)s')

soh = testutils.StdOutHandler()


def getTestUnit():
    return unit.Unit('mech', 'rebels')


def getTestCombat():
    return combat.Combat([unit.Unit('mech', 'rebels'),
                          unit.Unit('drone', 'autoarmy')])


def getTestCommand():
    return command.Command('punch')


class TestUnitModule(unittest.TestCase):
    """Unit tests for the unit module"""

    def testUnitDisplay(self):
        """Test of displaying unit information"""
        log.info('Starting unit display unit-test')

        newUnit = getTestUnit()
        self.assertEqual(newUnit.listCommands(), 'attack, armour')

        soh.hideStdOut()
        # Unit must be automated or test will hang for user input.
        self.assertTrue(newUnit.auto)
        newUnit.getChoice()
        soh.restoreStdOut()

    def testUnitMortality(self):
        """Unit test for testing unit mortality"""
        log.info('Starting unit mortality unit-test')

        newUnit = getTestUnit()

        #----------------------------------------------------------------------
        # Sets of actions.  Either a single action, or a list of actions.
        #
        # The second entry of the tuple is the expected end state.
        #----------------------------------------------------------------------
        actionSet = [(lambda: newUnit.kill(), unit.DEAD),
                     (lambda: newUnit.damageFraction(1), unit.DEAD),
                     (lambda: newUnit.damage(1), unit.OK),
                     (lambda: newUnit.damage(999), unit.DEAD),
                     ([lambda: newUnit.damage(1) for x in range(999)],
                      unit.DEAD),
                     ([lambda: newUnit.kill(),
                       lambda: newUnit.heal(1)],
                      unit.DEAD),
                     ([lambda: newUnit.kill(),
                       lambda: newUnit.healFraction(1)],
                      unit.DEAD)]

        for (actn, state) in actionSet:
            log.debug('Check action %d' % actionSet.index((actn, state)))

            # Ensure unit is in expected state.
            newUnit.reset()
            self.assertEqual(unit.OK, newUnit.state())

            # Impact unit with action(s).
            if isinstance(actn, (list, tuple)):
                log.debug('Do list of actions')
                for act in actn:
                    log.debug('Do action: \'%d\'' % actn.index(act))
                    act()
                    log.debug('State result: \'%s\'; health: \'%d\'' %
                              (newUnit.state(),
                               newUnit.attributes[unit.HP].value))
            else:
                log.debug('Do single action')
                actn()

            # Test final state is as expected.
            log.debug(('State expected: \'%s\'; '
                       'result: \'%s\'; health: \'%d\'') %
                      (state,
                       newUnit.state(),
                       newUnit.attributes[unit.HP].value))
            self.assertEqual(state, newUnit.state())

    def testVerifyUnits(self):
        """Unit test to verify custom units"""
        log.info('Starting custom unit verification')

        allIds = testutils.getKeys('custom/unit.ini')
        for thisId in allIds:
            log.info('Testing unit, ID: %s' % thisId)
            self.assertTrue(unit.Unit(thisId, 'rebels'))


class TestCommandModule(unittest.TestCase):
    """Unit tests for the command module"""

    def testVerifyCommands(self):
        """Unit test to verify custom commands"""
        log.info('Starting custom command verification')

        allIds = testutils.getKeys('custom/command.ini')
        for thisId in allIds:
            log.info('Testing command, ID: %s' % thisId)
            self.assertTrue(command.Command(thisId))

    def testGetTarget(self):
        """Unit test for getting a target"""
        log.info('Starting unit test for command targeting')

        newCmd = getTestCommand()
        newCbt = getTestCombat()
        newCmd.getTarget(newCbt.units, 'rebels', auto=True)


class TestTeamModule(unittest.TestCase):
    """Unit tests for the team module"""

    def testVerifyTeams(self):
        log.info('Starting custom team verification')

        allIds = testutils.getKeys('custom/team.ini')
        for thisId in allIds:
            log.info('Testing team, ID: %s' % thisId)
            self.assertTrue(team.Team(thisId))


class TestCombatModule(unittest.TestCase):
    """Unit tests for the combat module"""

    def testCombatSpin(self):
        """Test of combat spinning"""
        log.info('Starting basic spinning unit-test')

        newCombat = getTestCombat()

        def assertNextCombat():
            log.debug('Test next spin.')
            nextUnit = newCombat.spin()
            self.assertIsNotNone(nextUnit, 'Failed to generate unit on spin')
            return nextUnit

        firstUnit = assertNextCombat()
        firstList = newCombat.activelist()
        secondUnit = assertNextCombat()
        secondList = newCombat.activelist()

        self.assertNotEqual(firstUnit,
                            secondUnit,
                            'First two spins generated same unit')
        self.assertNotEqual(firstList,
                            secondList,
                            'First two spins did not change activelist')

        # Brute force test.  Ensure we can spin the combat for a large number
        # of cycles.
        for ii in range(2, 500):
            assertNextCombat()

    def testCombatUniqueNames(self):
        """Tests combat generates unique names only."""
        log.info('Starting unique name generation unit-test')

        units = []
        for ii in range(100):
            log.debug('Add unit no. %d' % ii)
            units.append(getTestUnit())

        # Setup two units with unique names
        UNIQ1 = 45
        UNIQ2 = 77
        units[UNIQ1].uniqueName = 'Specialish'
        units[UNIQ2].uniqueName = 'Specialish'

        combat.Combat(units)

        # Check that all units now have unique names
        names = []
        allUnique = True
        for unt in units:
            log.debug('Checking unit')
            if unt.name in names:
                log.error('Name {0} already used'.format(unt.name))
                allUnique = False
            else:
                log.debug('Name {0} not in use'.format(unt.name))
                names.append(unt.name)

        self.assertTrue(allUnique, 'Non-unique names generated in combat')
        self.assertEqual(units[UNIQ1].name,
                         'Specialish',
                         'First unique name changed')
        self.assertEqual(units[UNIQ2].name,
                         'Specialish1',
                         'Second unique name not changed correctly')

    def testCombatDisplay(self):
        """Test of displaying combat information"""
        log.info('Starting combat status unit-test')

        newUnit = getTestUnit()
        newCombat = getTestCombat()

        soh.hideStdOut()
        newCombat.printStatus()
        newCombat.printOrder()
        newCombat.printCommands(newUnit)
        soh.restoreStdOut()


class TestActionModule(unittest.TestCase):
    """Unit tests for the action module"""

    def testActionTypes(self):
        """Test action type verification"""
        log.info('Starting action type verification')

        self.assertTrue(action.Action(action.IMPACT))
        self.assertTrue(action.Action(action.BOOST))
        self.assertRaises(exceptions.ActionException,
                          action.Action, 'garbageactiontype')


class TestTimerModule(unittest.TestCase):
    """Unit tests for the timer module"""

    def testTimerInitiation(self):
        """Test of combat timer initiation"""
        log.info('Starting combat timer initiation')

        newEvent = event.Event(None, 0)
        self.assertTrue(newEvent, 'Failed to initialize new event')

    def testTimerExpiry(self):
        """Test of combat timer expiry"""
        log.info('Starting combat timer expiry')

        #----------------------------------------------------------------------
        # Test that a recurring timer reoccurs repeatedly.
        #----------------------------------------------------------------------
        newEvent = event.Event(None, 4, recurring=True)

        for num in range(0, 10):
            log.debug('Cycle %d / 9' % num)
            for cycle in range(0, 3):
                log.debug('Cycle %d' % cycle)
                self.assertEqual(newEvent.checkValid(), event.SILENT,
                                 'Timer popped when it should not have')
            self.assertEqual(newEvent.checkValid(), event.POP,
                             'Timer did not pop when it should have')

        #----------------------------------------------------------------------
        # Test that a non-recurring timer disappears.
        #----------------------------------------------------------------------
        newEvent = event.Event(None, 4)

        for num in range(0, 3):
            self.assertEqual(newEvent.checkValid(), event.SILENT,
                             'Timer popped when it should not have')
        self.assertEqual(newEvent.checkValid(), event.POP_DIE,
                         'Timer did not pop and die when it should have')


if __name__ == "__main__":
    for testClass in [TestCombatModule,
                      TestCommandModule,
                      TestTeamModule,
                      TestUnitModule,
                      TestActionModule,
                      TestTimerModule]:
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        unittest.TextTestRunner(verbosity=3).run(suite)
