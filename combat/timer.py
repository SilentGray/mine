#----------------------------------------------------------------------------- 
# Module: Timer
#-----------------------------------------------------------------------------
"""Contains class information on combat timers"""

# Python imports.
import logging as log

# Module imports.
import utils.counter as counter

SILENT = 0
POP = 1
POP_DIE = 2

class Timer:
    """Class for managing combat timers"""

    def __init__(self, object, count, recurring=False):
        """Initialise a new timer"""
        log.debug('Initializing new timer %s' % self)

        self.time = counter.Counter(count)
        self.subject = object
        self.recurring = recurring

    def expire(self):
        """Behaviour when a timer expires"""
        log.debug('Timer %s expired' % self)

        if self.recurring:
            self.time.reset()
            return POP
        else:
            return POP_DIE

    def checkValid(self):
        """Reduce and check the timer"""
        log.debug('Checking timer %s' % self)

        self.time.reduce(1)
        if self.time.getValue() is 0:
            return self.expire()
        return SILENT
