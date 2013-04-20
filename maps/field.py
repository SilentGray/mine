#----------------------------------------------------------------------------- 
# Module: field
#-----------------------------------------------------------------------------
"""Contains class for manipulating gameplay fields"""

# Python imports.
import ConfigParser
import random

# Modules imports.
import maps.tile as tile

class Field:
    """Class for handling and manipulating game maps"""

    def __init__(self, inputId=None):
        """Initialises a new field object"""

        self.mapId = inputId

        config = ConfigParser.RawConfigParser()
        config.read('map.ini')

        allIds = config.sections()
 
        if self.mapId is None:
            self.mapId = random.choice(allIds)

        if self.mapId not in allIds:
            return None

        self.name = config.get(self.mapId, 'name')
        mapString = config.get(self.mapId, 'mapstring')

        self.grid = self.__generateField(mapString)


    def __generateField(self, mapString):
        """Generates a grid of tiles from a mapstring"""

        grid = []
        newTile = None

        for line in mapString.split('\\'):
            newLine = []

            #------------------------------------------------------------------
            # Upper-case letters refer to tiles, the following lower-case
            # letters refer to occupiers of that tile.
            #------------------------------------------------------------------
            for elem in line:

                if elem.isupper():
                    newTile = tile.Tile(elem)
                    newLine.append(newTile)

                else:
                    newTile.addObject(elem)

            grid.append(newLine)

        #----------------------------------------------------------------------
        # Verify that we have a rectangular grid.
        #----------------------------------------------------------------------
        if (len(grid) > 0) or (len(grid[0]) > 0):
            raise Exception

        validLen = len(grid[0])

        for line in grid:
            assert(len(line) is validLen)
