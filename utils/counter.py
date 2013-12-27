#-----------------------------------------------------------------------------
# Module: Counter
#-----------------------------------------------------------------------------
"""Contains root class for handling counters"""

# Python imports
import logging as log

# Module imports
from utils.exceptions import CounterException


class Counter:
    """Class for handling and manipulating counters"""

    def __init__(self, numCount, initFull=True):
        """Initializes a new counter"""
        log.debug('Initialize a new counter.')
        numCount = int(numCount)

        self.maximum = numCount
        self.minimum = 0
        if initFull:
            log.debug('Initialise a full counter.')
            self.value = numCount
        else:
            log.debug('Initialize an empty counter.')
            self.value = 0

        self.default = self.value

    def _cleanup(self):
        """Clean-up value to a valid range"""
        log.debug('Clean-up a counter.')

        if self.value > self.maximum:
            log.debug('Decreasing value from %d to maximum.', self.value)
            self.value = self.maximum

        elif self.value < self.minimum:
            log.debug('Increasing value from %d to minimum.', self.value)
            self.value = self.minimum

    def getValue(self):
        """Returns the counter value"""
        log.debug('Returning the counter value')
        return(self.value)

    def reduce(self, amount, default=False):
        """Decrease the counter

        If the default flag is active then the default value is decremented.

        """
        log.debug('Decreasing a counter.')
        self.increase((-1 * amount), default)

    def increase(self, amount, default=False):
        """Increase a counter.

        If the default flag is active then the default value is incremented.

        """
        log.debug('Increasing a counter.')
        amount = int(amount)

        if default:
            log.debug('Changing default value')
            if (((self.default + amount) < self.minimum) or
                    ((self.default + amount) > self.maximum)):
                log.error('Default out of range')
                raise CounterException('Default incremented to {0}, over '
                                       'maximum of counter ({1})'.format(
                                           (self.default + amount),
                                           self.maximum))
            self.default += amount
        else:
            log.debug('Change regular value')
            self.value += amount
            self._cleanup()

    def min(self):
        """Minimise the counter"""
        log.debug('Minimise a counter.')

        self.value = self.minimum

    def reset(self):
        """Reset the counter"""
        log.debug('Resetting a counter.')

        self.value = self.default

    def reduceFraction(self, fraction):
        """Reduce the amount by a fraction"""
        log.debug('Reducing the counter by a fraction')

        newValue = self.value * (1 - fraction)
        self.value = int(newValue)

    def increaseFraction(self, fraction):
        """Increase the amount by a fraction"""
        log.debug('Increasing the counter by a fraction')

        newValue = self.value * (1 + fraction)
        self.value = int(newValue)
