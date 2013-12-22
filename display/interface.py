#-----------------------------------------------------------------------------
# Module: Interface
#-----------------------------------------------------------------------------
"""Module for handling interfaces"""

# Python imports.
import logging as log

# Module imports.
from utils.exceptions import InterfaceException

PROMPT = '>>  '
EDGE = '|'
SEPERATOR = '-'
BLANK = ' '


def printSpacer():
    """Prints a single spacer line"""
    print(EDGE + ('{:%s^78}' % SEPERATOR).format('') + EDGE)


def printText(text):
    """Prints a single block of text"""
    for line in text.split('\n'):
        print(EDGE + BLANK * 2 +
              ('{:%s<74}' % BLANK).format(line) +
              BLANK * 2 + EDGE)


def printBlank():
    """Prints a blank line"""
    print(EDGE + ('{:%s^78}' % BLANK).format('') + EDGE)


def printRefresh():
    """Print alot, to clear the terminal"""
    print(79 * '\n')


def printTwoColumns(text1, text2):
    """Prints two columns of text side-by-side"""
    lines1 = text1.split('\n')
    lines2 = text2.split('\n')
    max1 = len(lines1)
    max2 = len(lines2)

    for num in range(max([max1, max2])):
        if num < max1:
            string1 = lines1[num]
        else:
            string1 = ''
        if num < max2:
            string2 = lines2[num]
        else:
            string2 = ''

        print(EDGE + 2 * BLANK + ('{:%s<35}' % BLANK).format(string1) +
              4 * BLANK + ('{:%s<35}' % BLANK).format(string2) +
              2 * BLANK + EDGE)


def userInput(promptText, options):
    """Gets a users choice for an action"""
    log.debug('Get choice for action')

    choice = None
    while not choice:
        # Get user choice.
        printText('\n'.join([promptText,
                            '  ' + ', '.join([o.name for o in options])]))
        choice = _getInput()

        for option in options:
            # Case insensitive matching.
            if choice.lower() == option.name.lower():
                log.debug('Returning option: \'%s\'' % option.name)
                return option

        log.debug('Invalid response: \'%s\'' % choice)
        choice = None

    log.error('No valid option returned from user input: %s' % choice)
    raise InterfaceException


def _getInput():
    """Gets input"""
    response = input(EDGE + 2 * BLANK + PROMPT)
    log.debug('Got user input: \'%s\'' % response)
    return response
