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
import combat.combat as combat
import combat.unit as unit
import combat.command as command
import combat.timer as timer
import unittests.testutils.testutils as testutils

log.basicConfig(filename='logs/combattests.log',
                level=log.DEBUG,
                filemode='w',
                format='%(levelname)s >> %(message)s')

soh = testutils.StdOutHandler()

def getTestUnit():
    return unit.Unit('Mech')

def getTestCombat():
    return combat.Combat([unit.Unit('Mech')], [unit.Unit('Drone')])

def getTestCommand():
    return command.Command('punch')

class TestUnitModule(unittest.TestCase):
    """Unit tests for the unit module"""

    def testUnitDisplay(self):
        """Test of displaying unit information"""
        log.info('Starting unit display unit-test')

        newUnit = getTestUnit()
        self.assertEqual(newUnit.listCommands(), 'punch, armour')

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

        for (action, state) in actionSet:
            log.debug('Check action %d' % actionSet.index((action, state)))

            # Ensure unit is in expected state.
            newUnit.reset()
            self.assertEqual(unit.OK, newUnit.state())

            # Impact unit with action(s).
            if isinstance(action, (list, tuple)):
                log.debug('Do list of actions')
                for act in action:
                    log.debug('Do action: \'%d\'' % action.index(act))
                    act()
                    log.debug('State result: \'%s\'; health: \'%d\'' %
                              (newUnit.state(), newUnit.hitpoints.value))
            else:
                log.debug('Do single action')
                action()

            # Test final state is as expected.
            log.debug('State expected: \'%s\'; result: \'%s\'; health: \'%d\''%
                      (state, newUnit.state(), newUnit.hitpoints.value))
            self.assertEqual(state, newUnit.state())

    def testVerifyUnits(self):
        """Unit test to verify custom units"""
        log.info('Starting custom unit verification')

        allIds = testutils.getKeys('custom/unit.ini')
        for thisId in allIds:
            log.info('Testing unit, ID: %s' % thisId)
            self.assertTrue(unit.Unit(thisId))

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
        newCmd.getTarget([getTestUnit()], [getTestUnit()], auto=True)

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
        for ii in range (2, 500):
            assertNextCombat()

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

class TestTimerModule(unittest.TestCase):
    """Unit tests for the timer module"""

    def testTimerInitiation(self):
        """Test of combat timer initiation"""
        log.info('Starting combat timer initiation')

        newTimer = timer.Timer(None, 0)
        self.assertTrue(newTimer, 'Failed to initialize new timer')

    def testTimerExpiry(self):
        """Test of combat timer expiry"""
        log.info('Starting combat timer expiry')

        #----------------------------------------------------------------------
        # Test that a recurring timer reoccurs repeatedly.
        #----------------------------------------------------------------------
        newTimer = timer.Timer(None, 4, recurring=True)

        for num in range(0, 10):
            log.debug('Cycle %d / 9' % num)
            for cycle in range(0, 3):
                log.debug('Cycle %d' % cycle)
                self.assertEqual(newTimer.checkValid(), timer.SILENT,
                                 'Timer popped when it should not have')
            self.assertEqual(newTimer.checkValid(), timer.POP,
                            'Timer did not pop when it should have')

        #----------------------------------------------------------------------
        # Test that a non-recurring timer disappears.
        #----------------------------------------------------------------------
        newTimer = timer.Timer(None, 4)

        for num in range(0, 3):
            self.assertEqual(newTimer.checkValid(), timer.SILENT,
                             'Timer popped when it should not have')
        self.assertEqual(newTimer.checkValid(), timer.POP_DIE,
                        'Timer did not pop and die when it should have')

if __name__ == "__main__":
    for testClass in [TestCombatModule,
                      TestCommandModule,
                      TestUnitModule,
                      TestTimerModule]:
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        unittest.TextTestRunner(verbosity=3).run(suite)
