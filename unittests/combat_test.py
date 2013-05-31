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

class TestUnitModule(unittest.TestCase):
    """Unit tests for the unit module"""

    def testGetCommands(self):
        """Test of retrieving commands from a unit"""
        log.info('Starting unit commands unit-test')

        newUnit = getTestUnit()
        self.assertEqual(newUnit.listCommands(), 'punch, armour')

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
        log.info('Start custom command verification')

        allIds = testutils.getKeys('custom/command.ini')
        for thisId in allIds:
            log.info('Testing command, ID: %s' % thisId)
            self.assertTrue(command.Command(thisId))

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
        secondUnit = assertNextCombat()

        self.assertNotEqual(firstUnit,
                            secondUnit,
                            'First two spins generated same unit')

        # Brute force test.  Ensure we can spin the combat for a large number
        # of cycles.
        for ii in range (2, 500):
            assertNextCombat()

    def testCombatStatus(self):
        """Test of displaying combat status"""
        log.info('Starting combat status unit-test')

        newCombat = getTestCombat()
        soh.hideStdOut()
        newCombat.printStatus()
        soh.restoreStdOut()

    def testCommandsDisplay(self):
        """Test of displaying combat commands"""
        log.info('Starting combat command display unit-test')

        newCombat = getTestCombat()
        soh.hideStdOut()
        newCombat.printCommands(getTestUnit())
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
