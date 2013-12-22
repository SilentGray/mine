#-----------------------------------------------------------------------------
# Module: tile
#-----------------------------------------------------------------------------
"""Class for manipulating gameplay tiles"""

# Python imports
import logging as log
import configparser

# Module imports.
import maps.object as tileObj
import maps.hostile as hostile


class Tile:
    """Class for handling and manipulating game tiles"""

    def __init__(self, tileType='I'):
        """Initialises a new tile object"""
        log.debug('New tile, type: %s' % tileType)

        self.type = tileType
        self.display = '?'
        self.item = None
        self.hostile = None
        self.accessible = False

        self.__populate()

    def __populate(self):
        """Sets the default values for the tile"""
        log.debug('Populating tile with default values')

        config = configparser.ConfigParser()
        config.read('custom/tile.ini')

        self.display = config.get(self.type, 'display')

        access = config.get(self.type, 'access')
        if access.lower() == 'true' or access.lower() == 'yes':
            self.accessible = True
        else:
            self.accessible = False

    def addObject(self, objType):
        """Add an item or enemy that the tile contains"""
        log.debug(('Adding object %s to %s tile' % (objType, self.type)))

        config = configparser.ConfigParser()
        config.read('custom/object.ini')

        if objType in config.sections():
            log.debug('New object is an... object')
            if self.item:
                log.warning('New object %s overwrites previous tile item %s' %
                            (objType, self.item.type))
            self.item = tileObj.Object(objType)
            return

        config.read('custom/hostile.ini')

        if objType in config.sections():
            log.debug('New object is a hostile')
            if self.hostile:
                log.error('Cannot set multiple hostiles on same tile!')
                raise Exception
            self.hostile = hostile.Hostile(objType)
            return

        log.error('Unrecognised object: %s' % objType)
        raise Exception
