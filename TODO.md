###Todo

##Maps
#Add movement system __[LOW]__
Currently we cannot navigate maps, only display them.

##Units
#Decouple units from combat __[MED]__
Units should be stored in their own module outside of the combat logic.  To be done sooner to avoid issues later.

#Unit progression system __[LOW]__
User-owned units should be able to level up, getting new moves and increasing their stats.

##Combat
#Combat display __[HIGH]__
We need to display action information during combat.  (Eg. A attacks B for  X damage.)

# Retune combat #1 __[HIGH] >> SilentGray__
After addition of the new stats attacks need to be updated to accomodate these stats.  Each unit should have a normal attack based on stats, a `pass` move to skip a turn, as well as additional abilities.

#Retune combat #2 __[MED] >> SilentGray__
Existing abilities (armour) should be updated to use the new attributes.  This defines the interfaces that commands will use to:

* access units attributes
* add events to the combat (expirys, etc.)

#Items __[LOW]__
Characters should be able to equip items.  This should provide stat boosts to the holder as well as setting what the basic attack does (melee, ranged...).

#User input prompts should be capitalised __[LOW]__
Currently all user input is lower-case and input is detected with case-insensitivity.  It would be prettier if we display the names capitalised (eg. on the combat info screen).

#Add help commands __[LOW]__
There should be some additional commands to aid players.

* help           - displays commands available, and a basic description
* help <command> - gives information on a command
