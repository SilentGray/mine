import logging as log

import maps.field as fi
import combat.combat as co
import combat.unit as un
import display.interface as inf

log.basicConfig(filename='logs/mine.log',
                level=log.DEBUG,
                filemode='w',
                format='%(levelname)s >> %(message)s')

def printExit():
    print('')

def printHeader(text):
    printExit()
    print(text)
    print('')


f = fi.Field()
c = co.Combat([un.Unit('Mech', auto=False)], [un.Unit('Drone'),
                                              un.Unit('Drone')])

if False:
    printHeader('Field example')
    f.printMap()

    printHeader('Combat example')
    c.printStatus()
    c.printCommands(un.Unit('Mech'))

printHeader('Interactive Combat Test')
c.run()

printExit()

