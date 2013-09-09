#----------------------------------------------------------------------------- 
# Module: Event
#-----------------------------------------------------------------------------
"""Contains class information on combat events"""

# Python imports.
import logging as log

# Module imports.
import utils.counter as counter

# Timer types.
SILENT = 0
POP = 1
POP_DIE = 2

class Event:
    """Class for managing combat events"""

    def __init__(self, action, count, recurring=False):
        """Initialise a new event"""
        log.debug('Initializing new event %s' % self)

        self.time = counter.Counter(count)
        self.action = action
        self.recurring = recurring

    def expire(self):
        """Behaviour when a event expires"""
        log.debug('Event %s expired' % self)

        if self.recurring:
            self.time.reset()
            return POP
        else:
            return POP_DIE

    def checkValid(self):
        """Reduce and check the event timer"""
        log.debug('Checking event timer %s' % self)

        self.time.reduce(1)
        if self.time.getValue() is 0:
            return self.expire()
        return SILENT

    def turn(self, targets):
        """Executes the action of the event"""
        log.debug('Triggering action')

        # Do action.
