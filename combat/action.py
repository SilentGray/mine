#------------------------------------------------------------------------------
# Module: Action
#------------------------------------------------------------------------------
"""Contains action information.

The actions that are classed from the _Action_ class are of two groups.  Plain
actions are for performing behaviours, such as those required by commands.

Actions may also be held by events to performs these same behaviours at
specific times.

We support a number of potential action types.  These are:
   'melee'      - Melee-type attacks
   'ranged'     - Ranged-type attacks
   'buff'       - Direct impact on a units stat.
   'inactive'   - Special type; perform no action.

"""

# Python imports.
import logging as log
import random

# Module imports.
from utils.exceptions import ActionException
import combat.event as event

MELEE = 'melee'
RANGED = 'ranged'
BUFF = 'buff'
INACTIVE = 'inactive'

ACTIONTYPES = [MELEE, RANGED, BUFF, INACTIVE]
ATTACKTYPES = [MELEE, RANGED]


class Action(event.Event):
    """Class for manipulating and handling combat actions."""

    def __init__(self, command, caller, target):
        """Sets up a new action.

        _command_ is the command that the action is performing.
        _caller_ is the unit performing this action (if any).
        _target_ is the target unit this action is aimed at.

        Returns whether this action also serves as an event to be appended to
        the combatlist.

        """
        log.debug('Initializing a new action, type: {0}'.format(command.name))

        self.command = command
        self.caller = caller
        self.target = target

        self.setName()
        self.actionToDo = False
        self.delay = command.delay
        self.expiry = command.expiry

        if not (self.delay or self.expiry):
            log.debug('No delay or expiry')
            self.doAction()
            self.event = False
            return

        if self.delay:
            log.debug('Setup a delay for action')
            self.actionToDo = True
            expires = False
            if self.expiry:
                log.debug('Delay and expiry')
                expires = True

            event.Event.__init__(self, self.delay, recurring=expires)
            self.event = True
            return

        # Expiry only in effect.
        self.doAction()
        self.setName(expiry=True)
        event.Event.__init__(self, self.expiry, recurring=False)
        self.event = True

    def turn(self, targets):
        """Executes a turn of the action.

        This is one of:
        * We have had a delay, and now will implement the action
        * We have had an expiry period elapsed, and will now undo the action

        As we pre-picked the target, we ignore the _targets_ parameter.

        """
        log.debug('Turn of action')

        if self.actionToDo:
            log.debug('Action after delay')
            self.doAction()
            self.actionToDo = False

            # If we also need to expire the action then reset the timer.
            if self.expiry:
                log.debug('Reset timer for expiry of action')
                self.setName(expiry=True)
                event.Event.__init__(self, self.expiry, recurring=False)

            return

        # No action to do, so expire the earlier action.
        self.doExpire()

    def setName(self, expiry=False):
        """Sets an appropriate name for the action"""
        if expiry:
            mid = '-'.join([self.command.name, 'expiry'])
        else:
            mid = self.command.name
        self.name = '(' + mid + ')'

    def doAction(self):
        """Performs the action."""
        log.debug('Performing action %s on: %s' % (self.command.name,
                                                   self.target.name))

        if self.command.actionType == INACTIVE:
            log.debug('Action is %s' % INACTIVE)

            # Do nothing.

        elif self.command.actionType in ATTACKTYPES:
            log.debug('Action is %s' % self.command.actionType)

            self._calculateDamage(self.caller, self.target)
            log.info('{0} uses {1} on {2} for {3} damage'.format(
                self.caller.name,
                self.command.name,
                self.target.name,
                self.impact))
            self.target.damage(self.impact)

        elif self.command.actionType == BUFF:
            log.debug('Action is %s' % BUFF)

            self._buffAttribute()

            if self.impact:
                log.info('{0} uses {1} on {2} to change {3} by {4}'.format(
                         self.caller.name,
                         self.command.name,
                         self.target.name,
                         ', '.join(self.command.buffAttrs),
                         self.impact))
            else:
                log.info('{0} uses {1} on {2} with no impact'.format(
                    self.caller.name,
                    self.command.name,
                    self.target.name))

        else:
            log.debug('Unrecognised action type: %s' % self.command.actionType)
            raise ActionException('Unrecognised action type: %s' %
                                  self.command.actionType)

    def doExpire(self):
        """Expire the earlier action."""
        log.debug('Expiring action of {0} on {1}'.format(self.command.name,
                                                         self.target))

        if self.command.actionType == INACTIVE:
            log.debug('Expiry of {0}'.format(INACTIVE))

            # Do nothing.

        elif self.command.actionType in ATTACKTYPES:
            log.debug('Expiry of {0}'.format(self.command.actionType))
            self.target.heal(self.impact)

        elif self.command.actionType == BUFF:
            log.debug('Expiry of {0}'.format(BUFF))
            self._debuffAttribute()

        else:
            log.debug('Unrecognised action type: {0}'.format(
                self.command.actionType))
            raise ActionException('Unrecognised action type: {0}'.format(
                self.actionType))

        if self.command.expiryDescription:
            log.info(self.command.expiryDescription)

    def _calculateDamage(self, caller, target):
        """Calculates the impact on the target.

        Requires to specify the target and whether the attack is physical
        damage (reduced by defence) or not.

        Damage is calculated as the base damage of the attack incremented by
        the appropriate attack stat of the user scaled between 75 and 125%, and
        scaled by the target's defence.

        """
        log.debug('Calculating damage')

        basedmg = self.command.amount

        # Increment by the caller's attack
        if self.caller and self.command.actionType in ATTACKTYPES:
            log.debug('Add user-stat damage')

            scaler = random.randint(75, 125)
            log.debug('Scaler: {0}%'.format(scaler))

            callerdmg = (caller.getAttack(self.command.actionType) *
                         (scaler / 100))

        # Decrement by the target's defence
        targetdef = self.caller.getDefence() / 100

        self.impact = int((basedmg + callerdmg) * (1 - targetdef))
        log.debug('Damage calculated: "({0} + {1}) * (1 - {2}) = {3}"'.format(
            basedmg, callerdmg, targetdef, self.impact))

    def _buffAttribute(self):
        """Applies appropriate buffs to the target's attributes.

        This attempts to apply the total buff to each stat, up to the
        appropriate maximum and minimum.  When buffing the actual changes are
        recorded in a dictionary at _self.impact_ so that we can expire
        the changes later.

        """
        log.debug('Calculating buffs')

        baseBuff = self.command.amount

        self.impact = {}

        for attr in self.command.buffAttrs:
            log.debug('Acting on {0}'.format(attr))
            change = self.target.buff(attr, baseBuff)

            # Only record the value if a change occured.
            if change:
                self.impact[attr] = change

        log.debug('Final impact is: {0}'.format(self.impact))

    def _debuffAttribute(self):
        """Removes the buffs previously applied by this action.

        This checks the information recorded in _self.impact_ to do so.

        """
        log.debug('Applying debuffs')

        for attr in self.impact:
            log.debug('Debuff: {0}'.format(attr))
            self.target.buff(attr, (-1 * self.impact[attr]))
