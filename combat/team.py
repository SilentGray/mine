#------------------------------------------------------------------------------
# Module: Team
#------------------------------------------------------------------------------
"""Contains team information, including allied forces"""

# Python imports.
import logging as log
import configparser


class Team:
    """Class for handling team information"""

    def __init__(self, inputId):
        """Sets up a team object"""
        log.debug('New Team Object, ID: %s' % inputId)
        self.teamId = inputId

        config = configparser.ConfigParser()
        config.read('custom/team.ini')

        def getConfig(field):
            return config.get(self.teamId, field)

        self.allies = getConfig('allies').split(',')

        # Implicitly, we must be allied with our own team.
        if self.teamId not in self.allies:
            self.allies.append(self.teamId)

        self.name = self.teamId
        self.longName = getConfig('name')
