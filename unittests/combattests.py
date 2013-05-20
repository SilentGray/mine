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

log.basicConfig(filename='logs/combattests.log',
                level=log.DEBUG,
                filemode='w',
                format='%(levelname)s >> %(message)s')

class TestCombatModule(unittest.TestCase):
    """Unit tests for the combat module"""

    pass

class TestUnitModule(unittest.TestCase):
    """Unit tests for the unit module"""

    pass

if __name__ == "__main__":
    for testClass in [TestCombatModule,
                      TestUnitModule]:
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        unittest.TextTestRunner(verbosity=1).run(suite)
