import logging as log

import maps.field as fi
import combat.combat as co
import combat.unit as un

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
c = co.Combat([un.Unit('Mech', 'rebels', auto=False),
               un.Unit('Drone', 'autoarmy'),
               un.Unit('Drone', 'autoarmy')])

if False:
    printHeader('Field example')
    f.printMap()

    printHeader('Combat example')
    c.printStatus()
    c.printCommands(un.Unit('Mech', 'rebels'))

printHeader('Interactive Combat Test')
c.run()

printExit()
