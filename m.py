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
c = co.Combat([un.Unit('mech', 'rebels', auto=False),
               un.Unit('drone', 'autoarmy'),
               un.Unit('drone', 'autoarmy')])

if False:
    printHeader('Field example')
    f.printMap()

    printHeader('Combat example')
    c.printStatus()
    c.printCommands(un.Unit('mech', 'rebels'))

printHeader('Interactive Combat Test')
c.run()

printExit()
