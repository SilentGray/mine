###Todo

##Units
#Add new unit structure __[HIGH] [TL1]__
The current unit structures are too basic.  Units should have stats which are then used to determine move effectiveness etc.

An `attributes` object needs to be defined which contains counters for each stat.

Stats:

* Hitpoints - maximum hitpoints
* Attack <type> - attack strength and chance to hit
  * Melee
  * Ranged
* Defence - resistance to damage
* Evasion - chance to dodge
* Speed   - time taken between attacks

#Unit progression system __[LOW] dep: TL1__
User-owned units should be able to level up, getting new moves and increasing their stats.

##Combat
# Retune combat __[MED] dep: TL1__
After addition of the new stats attacks need to be updated to accomodate these stats.  Each unit should have a normal attack based on the equipped weapon, a `pass` move to skip a turn, as well as additional abilities.  Existing abilities should be updated to use the new attributes.

#Add help commands __[LOW]__
There should be some additional commands to aid players.

* help           - displays commands available, and a basic description
* help <command> - gives information on a command

#Add boost commands __[LOW] dep: TL1__
Currently the sample boost command `armour` is broken.  Boost commands for buffing stats should be implemented.
