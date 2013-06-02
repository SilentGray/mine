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

printHeader('Field example')
f = fi.Field()
f.printMap()

printHeader('Combat example')
c = co.Combat([un.Unit('Mech')], [un.Unit('Drone'), un.Unit('Drone')])
c.printStatus()
c.printCommands(un.Unit('Mech'))
inf.printPrompt()

printExit()
printExit()

