#----------------------------------------------------------------------------- 
# Script: minetests
#----------------------------------------------------------------------------- 
"""Unittest script for Mine"""

# Python imports.
import logging
import unittest

# Module imports.
import maps.field as field
import maps.hostile as hostile
import maps.object as object
import maps.tile as tile

logging.basicConfig(filename='mine.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(levelname)s >> %(message)s')

class TestMapsModule(unittest.TestCase):
    """Unit tests for the maps module"""

    def testBasicGridGeneration(self):
        """Unit test for generating grids from a basic mapstring"""

        self.assertTrue(field.Field('basic'))


    def testAddObjectToTile(self):
        """Unit test for adding multiple objects to tiles"""

        testTile = tile.Tile()
        self.assertTrue(testTile)

        testTile.addObject('p')
        testTile.addObject('s')
        with self.assertRaises(Exception):
            testTile.addObject('p')

        with self.assertRaises(Exception):
            testTile.addObject('s')


if __name__ == "__main__":
    for testClass in [TestMapsModule]:
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        unittest.TextTestRunner(verbosity=2).run(suite)