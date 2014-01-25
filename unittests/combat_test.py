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
import units.unit as unit
import combat.action as action
import combat.combat as combat
import combat.command as command
import combat.event as event
import combat.team as team
from unittests.testutils.testutils import (soh, getKeys,
                                           getTestUnit, getTestCombat)

log.basicConfig(filename='logs/combattests.log',
                level=log.DEBUG,
                filemode='w',
                format='%(levelname)s >> %(message)s')


class TestCommandModule(unittest.TestCase):
    """Unit tests for the command module"""

    def testVerifyCommands(self):
        """Unit test to verify custom commands"""
        log.info('Starting custom command verification')

        allIds = getKeys('custom/command.ini')
        for thisId in allIds:
            log.info('Testing command, ID: %s' % thisId)
            self.assertTrue(command.Command(thisId))

    def testGetTarget(self):
        """Unit test for getting a target"""
        log.info('Starting unit test for command targeting')

        newCmd = command.Command('attack')
        newCbt = getTestCombat()
        newCmd.getTarget(newCbt.units, 'rebels', auto=True)


class TestTeamModule(unittest.TestCase):
    """Unit tests for the team module"""

    def testVerifyTeams(self):
        log.info('Starting custom team verification')

        allIds = getKeys('custom/team.ini')
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

    def testCombatVictories(self):
        """Test of combat victory conditions.

        Do this by setting up combats in a victory condition, spin once and
        verify the correct winners are returned.

        """
        log.info('Starting combat victory unit-test')

        loser = unit.Unit('drone', 'autoarmy')
        winner = unit.Unit('drone', 'rebels')
        allUnits = [winner, loser]

        actionSet = [(lambda: loser.kill(), ['rebels']),
                     ([lambda: loser.kill(), lambda: winner.kill()], [])]

        for (actions, victors) in actionSet:
            log.debug('Run actionset...')

            for unt in allUnits:
                log.debug('Resetting {0}'.format(unt.name))
                unt.reset()
                self.assertEqual(unt.state(), unit.OK,
                                 'Unit not reset correctly during test')

            newCombat = combat.Combat([loser, winner])

            if isinstance(actions, (list, tuple)):
                for actn in actions:
                    actn()
            else:
                actions()

            soh.hideStdOut()
            result = newCombat.run()
            soh.restoreStdOut()

            self.assertEqual(victors, result,
                             ('Deathmatch victor returned "{0}"; expected '
                              '"{1}').format(result, victors))

    def testCombatComplete(self):
        """Run a test combat an ensure that it completes"""
        log.info('Starting complete combat unit-test')

        soh.hideStdOut()

        newCombat = getTestCombat()
        newCombat.run()

        soh.restoreStdOut()


class TestEventModule(unittest.TestCase):
    """Unit tests for the event module"""

    def testTimerInitiation(self):
        """Test of combat timer initiation"""
        log.info('Starting combat timer initiation')

        newEvent = event.Event(0)
        self.assertTrue(newEvent, 'Failed to initialize new event')

    def testTimerExpiry(self):
        """Test of combat timer expiry"""
        log.info('Starting combat timer expiry')

        #----------------------------------------------------------------------
        # Test that a recurring timer reoccurs repeatedly.
        #----------------------------------------------------------------------
        newEvent = event.Event(4, recurring=True)

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
        newEvent = event.Event(4)

        for num in range(0, 3):
            self.assertEqual(newEvent.checkValid(), event.SILENT,
                             'Timer popped when it should not have')
        self.assertEqual(newEvent.checkValid(), event.POP_DIE,
                         'Timer did not pop and die when it should have')


class TestActionModule(unittest.TestCase):
    """Unit tests for the action module"""

    unt = getTestUnit()

    def _attrChanged(self, attr):
        """Returns whether an attribute has been changed from its default"""
        if attr.value == attr.default:
            log.debug('Attribute at default value')
            return False
        else:
            log.debug('Attribute changed')
            return True

    def testActionNormal(self):
        """Test that a normal action damages a unit"""
        self.unt.reset()
        com = command.Command('attack')

        actn = com.activate(self.unt, self.unt)
        self.assertTrue(self._attrChanged(self.unt.attributes[unit.HP]),
                        'Attacked unit has not taken damage')

        self.assertTrue(actn is None,
                        'Command without delay or expiry added an event to '
                        'the combat')

    def testActionDelayed(self):
        """Test that a delayed action attacks after some time"""
        self.unt.reset()
        com = command.Command('heavy-swing')

        actn = com.activate(self.unt, self.unt)
        self.assertFalse(self._attrChanged(self.unt.attributes[unit.HP]),
                         'Command with delay hit immediately')

        self.assertTrue(actn is not None,
                        'Command with delay added action to combat')

        actn.turn(None)
        self.assertTrue(self._attrChanged(self.unt.attributes[unit.HP]),
                        'Command with delay did not hit')

    def testActionExpired(self):
        """Test that an acton expires correctly"""
        self.unt.reset()
        com = command.Command('armour')

        actn = com.activate(self.unt, self.unt)
        self.assertTrue(self._attrChanged(self.unt.attributes[unit.DEF]),
                        'Buff occurred immediately')
        self.assertTrue(actn is not None,
                        'Command with delay didn\'t return an event for the '
                        'combat')

        actn.turn(None)
        self.assertFalse(self._attrChanged(self.unt.attributes[unit.DEF]),
                         'Buff did not expire')

    def testActionDelayAndExpire(self):
        """Test an action that is delayed then expired"""
        self.unt.reset()
        com = command.Command('psyche-up')

        actn = com.activate(self.unt, self.unt)

        self.assertFalse(self._attrChanged(
            self.unt.attributes[unit.ATT][action.MELEE]),
            'Action incorrectly acted immediately')

        self.assertTrue(actn is not None,
                        'Command with delay didn\'t add an event to the '
                        'combat')

        actn.turn(None)
        self.assertTrue(self._attrChanged(
            self.unt.attributes[unit.ATT][action.MELEE]),
            'Action had no eventual impact')

        self.assertTrue(actn is not None,
                        'Command with expiry didn\'t add an event to the '
                        'combat after delay')

        actn.turn(None)
        self.assertFalse(self._attrChanged(
            self.unt.attributes[unit.ATT][action.MELEE]),
            'Action did not expire')


if __name__ == "__main__":
    for testClass in [TestCombatModule,
                      TestCommandModule,
                      TestActionModule,
                      TestTeamModule,
                      TestEventModule]:
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        unittest.TextTestRunner(verbosity=3).run(suite)
