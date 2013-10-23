#------------------------------------------------------------------------------
# Module: Action
#------------------------------------------------------------------------------
"""Contains action information.

The actions that are classed from the _Action_ class are of two groups.  Plain
actions are for performing behaviours, such as those required by commands.

Actions may also be held by events to performs these same behaviours at
specific times.

"""

# Python imports.
import logging as log

# Module imports.
from utils.exceptions import ActionException

#------------------------------------------------------------------------------
# We support a number of potential action types.
#    'impact'     - Direct impact on a units health (damage or
#                   healing).
#    'boost'      - Direct impact on a units stat.
#------------------------------------------------------------------------------
IMPACT = 'impact'
BOOST = 'boost'

class Action:
    """Class for manipulating and handling combat actions."""

    def __init__(self, actionType, amount=0):
        log.debug('Initializing a new action, type: %s, amount, %d' %
                  (actionType, amount))

        if actionType not in [IMPACT, BOOST]:
            log.error('Unrecognised action type: %s' % actionType)
            raise ActionException

        self.actionType = actionType
        self.amount = int(amount)

    def doAction(self, target):
        """Performs the action against the given target or targets.

        This acts directly upon the target.

        """
        log.debug('Performing action %s on: %s' % (self.name, target))

        if self.actionType == IMPACT:
            log.debug('Action is %s' % IMPACT)

            target.damage(self.amount)

        else:
            log.debug('Unrecognised action type: %s' % self.actionType)
            raise ActionException
