#----------------------------------------------------------------------------- 
# Module: field
#-----------------------------------------------------------------------------
"""Contains class for manipulating gameplay fields"""

# Python imports.
import configparser
import random
import logging as log

# Modules imports.
import maps.tile as tile

class Field:
    """Class for handling and manipulating game maps"""

    def __init__(self, inputId=None):
        """Initialises a new field object"""
        log.debug('New Field, ID: %s' % inputId)

        self.mapId = inputId

        config = configparser.ConfigParser()
        config.read('custom/map.ini')

        allIds = config.sections()
 
        if self.mapId is None:
            self.mapId = random.choice(allIds)
            log.debug('Random choice selected %s' % self.mapId)

        if self.mapId not in allIds:
            log.error('Unrecognised map ID: %s' % self.mapId)
            raise Exception

        self.name = config.get(self.mapId, 'name')
        mapString = config.get(self.mapId, 'mapstring')

        self.__generateField(mapString)


    def __generateField(self, mapString):
        """Generates a grid of tiles from a mapstring"""
        log.debug('Generating new field')
        log.info('Generating new map; %s' % self.name)

        self.grid = []
        newTile = None

        for line in mapString.split('\\'):
            log.debug('Parsing new map-line')
            newLine = []

            #------------------------------------------------------------------
            # Upper-case letters refer to tiles, the following lower-case
            # letters refer to occupiers of that tile.
            #
            # Whitespace is ignored.
            #------------------------------------------------------------------
            for elem in line:

                if elem == ' ':
                    log.debug('Ignoring whitespace')
                    continue

                if elem.isupper():
                    log.debug('Found new tile: %s' % elem)
                    newTile = tile.Tile(elem)
                    newLine.append(newTile)

                else:
                    log.debug('Found thing: %s' % elem)
                    newTile.addObject(elem)

            if len(newLine) > 0:
                self.grid.append(newLine)

        #----------------------------------------------------------------------
        # Verify that we have a rectangular grid.
        #----------------------------------------------------------------------
        try:
            assert(len(self.grid) > 0) and (len(self.grid[0]) > 0)

            validLen = len(self.grid[0])

            for line in self.grid:
                assert(len(line) is validLen)

        except:
            log.error('Grid for field %s is invalid!' % self.mapId)
            lengths = [len(length) for length in self.grid]
            log.error('Line lengths: ')
            log.error(lengths)
            raise Exception


    def printMap(self):
        """Print the grid contained by the field object"""
        log.info('Printing map for %s', self.name)

        if not self.grid:
            log.error('Loaded field %s has no containing data' % self.name)
            raise Exception

        spacer = '  '
        lineCount = 0
        for line in self.grid:

            print(spacer, end='')

            for tile in line:
                if tile.hostile:
                    elem = tile.hostile.display
                elif tile.item:
                    elem = tile.item.display
                else:
                    elem = tile.display

                print(elem, end='')

            if (lineCount % 5) is 0 or lineCount is 0:
                print(' < %d' % lineCount, end='')

            lineCount += 1
            print('')

        totalUnits = int(len(self.grid[0]) / 5) + 1
        print(spacer, end='')
        for unit in range(0, totalUnits):
            print('^    ', end='')
        print('\n' + spacer, end='')
        for unit in range(0, totalUnits):
            print('%-5d' % (unit * 5), end='')
        print('')

        return True
