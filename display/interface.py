#----------------------------------------------------------------------------- 
# Module: Interface
#----------------------------------------------------------------------------- 
"""Module for handling interfaces"""

def printSpacer():
    """Prints a single spacer line"""
    print('|' + '{:-^78}'.format('') + '|')

def printText(text):
    """Prints a single block of text"""
    for line in text.split('\n'):
        print('|  ' + ('{: <74}'.format(line)) + '  |')

def printBlank():
    """Prints a blank line"""
    print('|' + '{: ^78}'.format('') + '|')

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

        print('|  ' + ('{:<35}'.format(string1)) +
              '    ' + ('{:<35}'.format(string2)) + '  |')

def printPrompt():
    """Prints a prompt"""
    print('>>', end='  ')
