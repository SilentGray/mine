#-----------------------------------------------------------------------------
# Module: TestUtils
#-----------------------------------------------------------------------------
"""Utilites for testing"""

import sys
import os
import configparser

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

def getKeys(path):
    """Utility function for collecting all keys from a config file"""
    config = configparser.ConfigParser()
    config.read(path)
    return config.sections()
