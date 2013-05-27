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
import unittests.testutils.testutils as testutils

log.basicConfig(filename='logs/combattests.log',
                level=log.DEBUG,
                filemode='w',
                format='%(levelname)s >> %(message)s')

soh = testutils.StdOutHandler()

def testCombat():
    return combat.Combat([unit.Unit('Mech')], [unit.Unit('Drone')])

class TestUnitModule(unittest.TestCase):
    """Unit tests for the unit module"""

    def verifyUnits(self):
        """Unit test to verify custom units"""
        log.info('Starting custom unit verification')

        allIds = testutils.getKeys('custom/units.ini')
        for thisId in allIds:
            log.info('Testing unit, ID: %s' % thisId)
            self.assertTrue(unit.Unit(thisId))

class TestCombatModule(unittest.TestCase):
    """Unit tests for the combat module"""

    def testCombatSpin(self):
        """Test of combat spinning"""
        log.info('Starting basic spinning unit-test')

        newCombat = testCombat()

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

        # Brute force test.  Ensure we can spin the combat repeatedly.
        for ii in range (2, 500):
            assertNextCombat()

    def testCombatStatus(self):
        """Test of displaying combat status"""
        log.info('Starting combat status unit-test')

        newCombat = testCombat()
        soh.hideStdOut()
        newCombat.printStatus()
        soh.restoreStdOut()

    def testCombatCommandsDisplay(self):
        """Test of displaying combat commands"""
        log.info('Starting combat command display unit-test')

        newCombat = testCombat()
        soh.hideStdOut()
        newCombat.printCommands()
        soh.restoreStdOut()

if __name__ == "__main__":
    for testClass in [TestCombatModule,
                      TestUnitModule]:
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        unittest.TextTestRunner(verbosity=1).run(suite)
