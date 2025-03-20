# Analysis of Quest Design and Player Exploration in Open-World Games

## Datasets
    
### Locations Data
A set of discoverable locations in Bethesda's _The Elder Scrolls V: Skyrim_ along with the Hold the location belongs to and the location's X and Y coordinates
as described by _The Unofficial Elder Scrolls Pages_'s [Skyrim Gamemap](https://gamemap.uesp.net/sr/?world=skyrim&layer=day&x=28700&y=-53550&zoom=1.914)

Only locations from the base game world map are included. This means locations specific to any DLC and locations that exist outside the confines of the world map are not included, but the latter will still be accounted for wherever necessary.

### Quest Data
A set of quests in Bethesda's _The Elder Scrolls V: Skyrim_ which includes the quest's title, the title of the quest line it belongs to, any prerequisite quests (delimited by "." in the case of multiple prerequisites), and the set of locations that the quest has the player visit (again delimited by "."), all taken from _The Unofficial Elder Scrolls Pages_'s [Skyrim Quest Wiki](https://en.uesp.net/wiki/Skyrim:Quests)

The questlines included are: 
- Main Quest
- College of Winterhold
- Companions
- Dark Brotherhood
- Imperial Legion
- Stormcloaks
- Thieves Guild
- Daedric Quest(s)
- Side Quest(s)
- Master Skill Quest(s)

Any quests introduced by DLC are excluded from this set, along with miscellaneous quests which have one or more properties that make them unsuitable for this analysis. Specifically, quests that involve collecting materials that can be found throughout the game world and are not unique. These quests may be included if they are part of a larger questline and, in these cases, only the location of the quest-giver will be listed. Additionally, quests that only take place in one location, such as most quests associated with dungeons, will not be included.

Quests that involve radiant locations, locations that are randomly selected when the quest is given, will be considered on a case-by-case basis. If the radiant locations for the quest are finite in number (and reasonable to enumerate), then every enumeration of the quest with radiant locations will be included and labeled as follows:

>{Quest Name} (Radiant *n*/*m*)

where *n* = the enumeration, and *m* = the total number of enumerations (i.e. the number of radiant locations the quest is selecting from). In the graph, edges for quests with radiant locations will be weighted with 1/*m*.