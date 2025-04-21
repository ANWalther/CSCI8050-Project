# Analysis of Quest Design and Player Exploration in Open-World Games

## Project Dependencies
[networkx](https://networkx.org/)

[matplotlib](http://matplotlib.org/)

## Datasets
    
### Locations Data
A set of discoverable locations in Bethesda's _The Elder Scrolls V: Skyrim_ along with the Hold the location belongs to and the location's X and Y coordinates
as described by _The Unofficial Elder Scrolls Pages_'s [Skyrim Gamemap](https://gamemap.uesp.net/sr/?world=skyrim&layer=day&x=28700&y=-53550&zoom=1.914)

Only locations from the base game world map are included. This means locations specific to any DLC and locations that exist outside the confines of the world map are not included, but the latter will still be accounted for wherever necessary.

### Quest Data
A set of quests in Bethesda's _The Elder Scrolls V: Skyrim_ which includes the quest's title, the title of the quest line it belongs to, any prerequisite quests (delimited by "." in the case of multiple prerequisites), and the set of locations that the quest has the player visit (again delimited by "."), all taken from _The Unofficial Elder Scrolls Pages_'s [Skyrim Quest Wiki](https://en.uesp.net/wiki/Skyrim:Quests)

Any quests introduced by DLC are excluded from this set, along with miscellaneous quests which have one or more properties that make them unsuitable for this analysis. Specifically, quests that involve collecting materials that can be found throughout the game world and are not unique. These quests may be included if they are part of a larger questline and, in these cases, only the location of the quest-giver will be listed. Additionally, quests that only take place in one location, such as most quests associated with dungeons or those that send the player throughout one city, will not be included. This is both for simplicity, and because these quests generally do no lead to the discovery of new locations, which is the ultimate research goal for this project.

The questlines included are: 
- Main Quest
- College of Winterhold
- Companions
    - radiant quests excluded due to large number of possible locations
- Dark Brotherhood
    - radiant quest The Dark Brotherhood Forever involves two radiant locations from a possible list of 12, meaning roughly 60 possibile variations and so is excluded
- Imperial Legion
- Stormcloaks
- Thieves Guild
    - Delvin's jobs (Numbers, Fishing, and Bedlam) have been consolidated as one radiant quest named "Delvin's Jobs"
    - Vex's jobs (Burglary, Shill, Sweep, and Heist) have been consolidated as one radiant quest named "Vex's Jobs"
- Daedric Quest(s)
- Side Quest(s)
    - radiant quest The Words of Power is excluded due to its large number of possible locations (31 total)
    - radiant bounty quests, which can be given by any inkeeper NPC, jarl NPC, or steward NPC or a hold, are also excluded due to the large number of possible locations



Quests that involve radiant locations, locations that are randomly selected when the quest is given, will be considered on a case-by-case basis. If the radiant locations for the quest are finite in number (and reasonable to enumerate), then the static locations for the quest will be listed with the original quest name. Every enumeration of the quest's radiant locations will list this original quest as a prerequisite and be labeled as follows:

>{Quest Name} (Radiant *n*/*m*)

where *n* = the enumeration, and *m* = the total number of enumerations (i.e. the number of radiant locations the quest is selecting from). This ensures that radiant locations are not connected together, as the radiant locations have no relationship with one another, but are still connected to the quest's other locations. This also allows radiant quests to be included in larger quest lines without requiring the next quest in the questline to list each radiant variation as a prerequisite. There is a notable drawback in that these radiant locations are not connected to the locations of the next quest in the questline. However, most quests utilizing radiant locations require the player to return to the location they were given the quest before moving on, so this should not impact the analysis in an overly negative way.

