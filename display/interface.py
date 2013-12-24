#-----------------------------------------------------------------------------
# Module: Interface
#-----------------------------------------------------------------------------
"""Module for handling interfaces

This handles the output we recieve from Mine.  This means handling the
formatting of the output in both form and colours.

This will eventually support 8 and 256 colours, but for now only 256-colours
have been implemented.
"""

# Python imports.
import logging as log

# Module imports.
from utils.exceptions import InterfaceException


class InvalidColours(InterfaceException):
    pass

INVALID_COLOUR_VALUE = 'Attempted to set colour %d, only %d available.'

# What colours to use for what.
#
# Set the appropriate colour function.  This should select the appropriate
# scheme in the future, but for now hardcode the choice here.
clrs = 0


def colour_0(value, back):
    """Dummy function for callbacks that attempt to set colour with no
    colours in use."""
    return('')


def colour_8(value, back):
    """Sets a 8-colour value.  Sets text colour, or background colour."""
    if value >= 8:
        raise InvalidColours(INVALID_COLOUR_VALUE % (value, 8))
    if back:
        key = 4
    else:
        key = 3
    return('\033[%d%dm' % (key, value))


def colour_256(value, back):
    """Sets a 256-colour value.  Sets text colour, or background colour."""
    if value >= 256:
        raise InvalidColours(INVALID_COLOUR_VALUE % (value, 256))
    if back:
        key = 48
    else:
        key = 38
    return('\033[%d;05;%dm' % (key, value))

if clrs == 256:
    colour = colour_256
    BACK_NORM = 234
    BACK_HIGHLIGHT = 244
    FORE_NORM = 251
    FORE_SUBDUED = 242
    FORE_HIGHLIGHT = 255
elif clrs == 8:
    colour = colour_8
    BACK_NORM = 0
    BACK_HIGHLIGHT = 4
    FORE_NORM = 6
    FORE_SUBDUED = 2
    FORE_HIGHLIGHT = 7
else:
    colour = colour_0
    BACK_NORM = 0
    BACK_HIGHLIGHT = 0
    FORE_NORM = 0
    FORE_SUBDUED = 0
    FORE_HIGHLIGHT = 0

# What symbols to use for what.
PROMPT = '>>  '
EDGE = '|'
SEPERATOR = '-'
BLANK = ' '


# Colour application.
def bold():
    """Sets the font to be bold."""
    return('\033[1m')


def applyColour(value, back=False):
    """Sets a colour, accomodating for colours available."""
    log.debug('Apply colour: %d' % value)
    return(colour(value, back))


def applyColours(fore_col, back_col):
    """Sets both fore and background colours."""
    log.debug('Apply colours: Fore=%d, Back=%d' % (fore_col, back_col))
    return(applyColour(fore_col, False) + applyColour(back_col, True))


def hightlitColours(fore_col=FORE_HIGHLIGHT, back_col=BACK_NORM):
    """Sets text and background colours and applies a bold font."""
    log.debug('Apply colours: Set highlighted colours; Fore=%d, Back=%d' %
              (fore_col, back_col))
    return(bold() + applyColours(fore_col, back_col))


def subduedColours():
    """Resets the text and background colours to subdued."""
    log.debug('Apply colours: Set subdued colours.')
    return(applyColours(FORE_SUBDUED, BACK_NORM))


def resetColours():
    """Resets the text and background colours to default."""
    log.debug('Apply colours: Set default formatting.')
    return(applyColours(FORE_NORM, BACK_NORM))


def cleanColours():
    """Removes all formatting."""
    log.debug('Apply colours: Remove text formatting.')
    return('\033[0m')

# Format definitions.
INTLINESTART = (subduedColours() + EDGE + resetColours())
INTLINEEND = (subduedColours() + EDGE)


def printLine(line, padding=True):
    """Prints the line and handles edge formatting."""
    if padding:
        print(INTLINESTART + 2 * BLANK + line + 2 * BLANK + INTLINEEND)
    else:
        print(INTLINESTART + line + INTLINEEND)


def printRefresh():
    """Print to clear the screen and reset cursor."""
    print('\033[2J\033[h')
    return


def printSpacer():
    """Prints a single spacer line"""
    printLine((subduedColours() + ('{:%s^78}' % SEPERATOR).format('')),
              padding=False)


def printText(text):
    """Prints a single block of text"""
    for line in text.split('\n'):
        printLine(('{:%s<74}' % BLANK).format(line))


def printBlank():
    """Prints a blank line"""
    printLine(('{:%s^74}' % BLANK).format(''))


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

        printLine(('{:%s<35}' % BLANK).format(string1) + 4 * BLANK +
                  ('{:%s<35}' % BLANK).format(string2))


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
    response = input(INTLINESTART +
                     2*BLANK +
                     subduedColours() +
                     PROMPT +
                     resetColours())
    response = response.strip()
    log.debug('Got user input: \'%s\'' % response)
    return response
