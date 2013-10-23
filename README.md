#Mine

Mine is a text-based RPG engine, built for use in a terminal.  It is currently in-development and contains rudimentary frameworks rather than a 'battle-ready' program.

Mine is designed to run on python3.

##'Screenshots'
###Combat

```
|------------------------------------------------------------------------------|
|                                                                              |
|  -- Automated Army Forces --                                                 |
|  Rogue Drone    : 0/10                  Rogue Drone    : 10/10               |
|    Status: Dead                           Status: OK                         |
|                                                                              |
|  -- Rebel Alliance --                                                        |
|  Mechanical Suit: 45/50                                                      |
|    Status: OK                                                                |
|                                                                              |
|  Upcoming turns:                                                             |
|    Rogue Drone, Rogue Drone                                                  |
|                                                                              |
|------------------------------------------------------------------------------|
|  Commands available to Mechanical Suit:                                      |
|    punch, armour                                                             |
|  >>
```

###Navigation

```
  ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| < 0
  |||||||||||||||||||||||||...........................|||||||
  |||||||||..............................................||||
  ||.......................................s...............||
  |.........................................................|
  |...............................||||||||||||.............|| < 5
  ||.........................|||||||||||||||||||.........||||
  |||||..................|||||||||||........||||||.....||||||
  ||||||...............||||||||||.......s..............||||||
  |||||||||||....||||||||||||||||||||........|||.....||||||||
  ||||||||||||||||||||||||.....|||||||||||||||||[...[|||||||| < 10
  ||||||||||||||||||||....[.......|||||||||||||||..||||||||||
  ||||||||||||||||.............[.......|||||||....|||||||||||
  |||||||||||||...[..s.........................||||||||||||||
  |||||||||||||||......[..s.....|||||||||||||||||||||||||||||
  |||||||||||||||||||........|||||||||||||||||||||||||||||||| < 15
  |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
  ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    
  0    5    10   15   20   25   30   35   40   45   50   55   
```

##Available features
###Combat system
Mine contains a rudimental, if flexible, combat system.  This is akin to traditional RPG combat and implements a time-based field of battle.

Unlike more traditional RPGs this system is capable of extending to a larger number of combatants and a larger number of 'teams' within a fight - limited only by the decisions of the designer.

###Map navigation system
Mine has an initial design of a tile-based navigational system.  Currently this only extends to generating a map, rather than navigating it.
