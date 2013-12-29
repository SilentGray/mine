#-----------------------------------------------------------------------------
# Module: TestUtils
#-----------------------------------------------------------------------------
"""Utilites for testing"""

# Python imports.
import sys
import os
import configparser

# Module imports.
import units.unit as unit
import combat.combat as combat


class StdOutHandler():
    """Class for managing stdout"""

    def __init__(self):
        self.oldStdout = None

    def hideStdOut(self):
        self.oldStdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def restoreStdOut(self):
        if self.oldStdout:
            sys.stdout.close()
            sys.stdout = self.oldStdout

soh = StdOutHandler()


def getKeys(path):
    """Utility function for collecting all keys from a config file"""
    config = configparser.ConfigParser()
    config.read(path)
    return config.sections()


def getTestUnit():
    """Get a basic unit for testing"""
    return unit.Unit('mech', 'rebels')


def getTestCombat():
    """Get a basic combat for testing"""
    return combat.Combat([unit.Unit('drone', 'rebels'),
                          unit.Unit('drone', 'autoarmy')])
