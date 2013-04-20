#----------------------------------------------------------------------------- 
# Module: tile
#-----------------------------------------------------------------------------
"""Class for manipulating gameplay tiles"""

import ConfigParser
import maps.object as TileObj

class Tile:
    """Class for handling and manipulating game tiles"""

    def __init__(self, tileType='i'):
        """Initialises a new tile object"""

        self.type = tileType
        self.display = '?'
        self.item = None
        self.hostile = None
        self.accessible = False

        self.__populateType()


    def __populate(self):
        """Sets the default values for the tile"""

        config = ConfigParser.RawConfigParser()
        config.read('tile.ini')

        self.display = config.get(self.type, 'display', '?')

        access = config.get(self.type, 'access', 'False')
        if access.lower() == 'true' or access.lower() == 'yes':
            self.accessible = True
        else:
            self.accessible = False


    def addObject(self, objType):
        """Add an item or enemy that the tile contains"""

        newObj = TileObj.Object(objType)

        if newObj.type = 'Item':
            self.isItem = newObj

        elif newObj.type = 'Hostile':
            self.hostile = newObj