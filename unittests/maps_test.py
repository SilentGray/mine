#----------------------------------------------------------------------------- 
# Script: mapstests
#----------------------------------------------------------------------------- 
"""Unittest script for map functions"""

# Python imports.
import logging as log
import unittest
import sys
import configparser

sys.path.append('.')

# Module imports.
import maps.field as field
import maps.hostile as hostile
import maps.object as object
import maps.tile as tile
import unittests.testutils.testutils as testutils

log.basicConfig(filename='logs/mine.log',
                level=log.DEBUG,
                filemode='w',
                format='%(levelname)s >> %(message)s')
soh = testutils.StdOutHandler()

class TestFieldsModule(unittest.TestCase):
    """Unit tests for the fields module"""

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
        soh.hideStdOut()
        self.assertTrue(newField.printMap())
        soh.restoreStdOut()

    def verifyGrids(self):
        """Unit test to verify custom maps"""
        log.info('Starting custom map verification')

        allIds = testutils.getKeys('custom/maps.ini')

        for thisId in allIds:
            log.info('Testing map, ID: %s' % thisId)
            self.assertTrue(field.Field(thisId))

class TestTilesModule(unittest.TestCase):
    """Unit tests for the tiles module"""

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

class TestHostileModule(unittest.TestCase):
    """Unit tests for the hostile module"""

    pass

class TestObjectModule(unittest.TestCase):
    """Unit tests for the object module"""

    pass

if __name__ == "__main__":
    for testClass in [TestFieldsModule,
                      TestTilesModule,
                      TestHostileModule,
                      TestObjectModule]:
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        unittest.TextTestRunner(verbosity=1).run(suite)