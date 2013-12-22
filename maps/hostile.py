#------------------------------------------------------------------------------
# Module: hostile
#------------------------------------------------------------------------------
"""Class for generating and accessing hostile information"""

# Python imports.
import logging as log
import configparser


class Hostile():
    """Class for handling and manipulating hostile objects"""

    def __init__(self, hostType):
        """Initisalises a new hostile object"""
        log.debug('New hostile, type: %s' % hostType)

        config = configparser.ConfigParser()
        config.read('custom/hostile.ini')

        self.name = config.get(hostType, 'name')
        self.display = config.get(hostType, 'display')
