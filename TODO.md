###Todo

##Maps
#Add movement system __[LOW]__
Currently we cannot navigate maps, only display them.

##Units
#Decouple units from combat __[MED] [TL1]__
Units should be stored in their own module outside of the combat logic.  To be done sooner to avoid issues later.  The additional combat behaviour is then a class extension in the combat module.

#Unit progression system __[LOW] dep: TL1__
User-owned units should be able to level up, getting new moves and increasing their stats.

##Combat
#Combat display __[HIGH]__
We need to display action information during combat.  (Eg. A attacks B for X damage.)

#Combat delays __[MED]__
Currently there are no commands (and no unit-tests) using either delays.  These should be added and regressably testable.

Unit tests for this behaviour have been added, and are currently failing.

#Items __[LOW]__
Characters should be able to equip items.  This should provide stat boosts to the holder as well as setting what the basic attack does (melee, ranged...).

#User input prompts should be capitalised __[LOW]__
Currently all user input is lower-case and input is detected with case-insensitivity.  It would be prettier if we display the names capitalised (eg. on the combat info screen).

#Add help commands __[LOW]__
There should be some additional commands to aid players.

* help           - displays commands available, and a basic description
* help <command> - gives information on a command
