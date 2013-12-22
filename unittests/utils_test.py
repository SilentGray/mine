#-----------------------------------------------------------------------------
# Script: utiltests
#-----------------------------------------------------------------------------
"""Unittest script for util functions"""

# Python imports
import logging as log
import unittest
import sys

sys.path.append('.')

# Module imports.
import utils.counter as counter

log.basicConfig(filename='logs/utiltests.log',
                level=log.DEBUG,
                filemode='w',
                format='$(levelname)s >> %(message)s')


class TestCounterModule(unittest.TestCase):
    """Unit tests for the counter module"""

    def testBasicCounter(self):
        """Test of basic counter function"""
        log.info('Starting basic counter unit-test')

        newCounter = counter.Counter(100)
        self.assertEqual(newCounter.getValue(), 100)
        newCounter.reset()
        self.assertEqual(newCounter.getValue(), 100)

        newCounter = counter.Counter(100, initFull=False)
        self.assertEqual(newCounter.getValue(), 0)
        newCounter.reset()
        self.assertEqual(newCounter.getValue(), 0)

    def testBasicArith(self):
        """Test of basic arithmetic"""
        log.info('Starting basic arithmetic unit-test')

        newCounter = counter.Counter(100)
        newCounter.reduce(50)
        self.assertEqual(newCounter.getValue(), 50)

        newCounter.increase(100)
        self.assertEqual(newCounter.getValue(), 100)

        newCounter.reduce(100)
        self.assertEqual(newCounter.getValue(), 0)

        newCounter.reset()
        newCounter.reduceFraction(0.25)
        self.assertEqual(newCounter.getValue(), 75)

        newCounter.reduceFraction(0.25)
        self.assertEqual(newCounter.getValue(), 56)

if __name__ == "__main__":
    for testClass in [TestCounterModule]:
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        unittest.TextTestRunner(verbosity=1).run(suite)
