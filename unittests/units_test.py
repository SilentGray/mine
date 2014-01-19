#-----------------------------------------------------------------------------
# Script: units_tests
#-----------------------------------------------------------------------------
"""Unittest script for unit functions"""

# Python imports.
import logging as log
import unittest
import sys

sys.path.append('.')

# Module imports.
import units.unit as unit
from unittests.testutils.testutils import (soh, getKeys, getTestUnit)

log.basicConfig(filename='logs/unitstests.log',
                level=log.DEBUG,
                filemode='w',
                format='%(levelname)s >> %(message)s')


class TestUnitModule(unittest.TestCase):
    """Unit tests for the unit module"""

    def testUnitCommands(self):
        """Test unit command generation"""
        log.info('Starting unit commands unit-test')

        newUnit = getTestUnit()

        def checkCommand(command):
            """Check for the presence of a particular command"""
            log.debug('Check command: {0}'.format(command))
            self.assertTrue(len([cmd for cmd in newUnit.commands
                                 if cmd.name == command]) > 0,
                            'Command "{0}" not owned by test unit'.format(
                                command))

        for cmd in ['attack', 'armour', 'pass']:
            checkCommand(cmd)

    def testUnitDisplay(self):
        """Test of displaying unit information"""
        log.info('Starting unit display unit-test')

        newUnit = getTestUnit()
        self.assertEqual(newUnit.listCommands(), 'attack, armour, pass')

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
                for act in actn:
                    act()
            else:
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

        allIds = getKeys('custom/unit.ini')
        for thisId in allIds:
            log.info('Testing unit, ID: %s' % thisId)
            self.assertTrue(unit.Unit(thisId, 'rebels'))

if __name__ == "__main__":
    for testClass in [TestUnitModule]:
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        unittest.TextTestRunner(verbosity=3).run(suite)
