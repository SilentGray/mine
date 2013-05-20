#----------------------------------------------------------------------------- 
# Script: minetests
#----------------------------------------------------------------------------- 
"""Unittest script for Mine"""

# Python imports.
import logging as log
import unittest
import sys
import os

# Module imports.
import maps.field as field
import maps.hostile as hostile
import maps.object as object
import maps.tile as tile

log.basicConfig(filename='mine.log',
                level=log.DEBUG,
                filemode='w',
                format='%(levelname)s >> %(message)s')

class TestMapsModule(unittest.TestCase):
    """Unit tests for the maps module"""

    def testBasicGridGeneration(self):
        """Unit test for generating grids from a basic mapstring"""
        log.info('Starting grid-generation unit-test')

        self.assertTrue(field.Field('basic'))


    def testBasicGridDisplay(self):
        """Unit test for printing a basic grid"""
        log.info('Starting grid-printing unit-test')

        newField = field.Field('basic')

        #----------------------------------------------------------------------
        # Print the map to /dev/null, not the test.
        #----------------------------------------------------------------------
        oldStdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        self.assertTrue(newField.printMap())
        sys.stdout.close()
        sys.stdout = oldStdout


    def testAddObjectToTile(self):
        """Unit test for adding multiple objects to tiles"""
        log.info('Starting object allocation unit-test')

        testTile = tile.Tile()
        self.assertTrue(testTile)

        testTile.addObject('p')
        testTile.addObject('s')

        log.debug('Adding too many objects')
        with self.assertRaises(Exception):
            testTile.addObject('p')

        log.debug('Adding too many hostiles')
        with self.assertRaises(Exception):
            testTile.addObject('s')


if __name__ == "__main__":
    for testClass in [TestMapsModule]:
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        unittest.TextTestRunner(verbosity=1).run(suite)