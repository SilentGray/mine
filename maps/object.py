#----------------------------------------------------------------------------- 
# Module: object
#-----------------------------------------------------------------------------
"""Class for generating and accessing enemy and item information"""

import ConfigParser

class Object:
    """Class for handling and manipulating objects"""

    def __init__(self, objType=None):
        """Initializes a new object"""

        config = ConfigParser.RawConfigParser()
        config.read('object.ini')

        self.type = config.get(objType, 'type')


class Hostile(Object):
    """Class for storing and retrieving hostile information"""


class Item(Object):
    """Class for storing and retrieving item information"""