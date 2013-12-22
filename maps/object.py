#-----------------------------------------------------------------------------
# Module: object
#-----------------------------------------------------------------------------
"""Class for generating and accessing object information"""

# Python imports.
import configparser
import logging as log


class Object:
    """Class for handling and manipulating objects"""

    def __init__(self, objType=None):
        """Initializes a new object"""
        log.debug('New Object, type: %s' % objType)

        config = configparser.ConfigParser()
        config.read('custom/object.ini')

        self.name = config.get(objType, 'name')
        self.isDecorative = config.get(objType, 'decorative')
        self.display = config.get(objType, 'display')
