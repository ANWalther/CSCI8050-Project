import networkx as nx
import csv

class Quest:
    def __init__(self, name:str, questline:str, prerequisites:str, locations:str):
        self.name = name
        self.questline = questline
        self.locations = locations.split(".")

        if prerequisites.lower() == "none":
            self.prerequisites = []
        else:
            self.prerequisites = prerequisites.split(".")
        #self.quest_weight = 1
    
    def __str__(self):
        return "{" + self.name + ", " + self.questline + ", " + str(self.prerequisites) + ", " + str(self.locations) + "}"

locations_data_file = "data/skyrim-locations.csv"
quests_data_file = "data/skyrim-quests.csv"

def ReadLocations():
    locations_graph = nx.Graph()
    with open(locations_data_file, 'r') as locations_data:
        locations = csv.DictReader(locations_data)
        for location in locations:
            name = location['LOCATION_NAME']
            x = float(location['X_COORD'])
            y = float(location['Y_COORD'])
            locations_graph.add_node(name, hold=location['HOLD'], x_coord=x, y_coord=y)
    
    return locations_graph
    
def ReadQuests():
    quest_list = []
    with open(quests_data_file, 'r') as quests_data:
        quests = csv.DictReader(quests_data)
        for quest in quests:
            name = quest['QUEST_NAME']
            line = quest['QUESTLINE']
            prereq = quest['PREREQUISITE_QUEST']
            locations = quest['LOCATIONS']
            quest_list.append(Quest(name, line, prereq,locations))
    
    return quest_list

def main():

    print("Reading locations data")

    locationGraph = ReadLocations()

    print("Locations data finished\n")
    #print(locationGraph.nodes(True))
    print()
    print("Reading quests data")

    questsData = ReadQuests()

    print("Quests data finished\n")
    #for q in questsData:
        #print(q)

    # 2. read quest data, however some quests use other quests as prerequisites, and their order is not guaranteed.
    #    to account for this, first put all quests into a queue for processing. If a quest's prerequisite hasn't been processed, throw it to the end of the queue
    #    if the quest is reached in the queue a second time and the prerequisite still hasn't been processed, discard it as bad data

    # 3. for interest reasons, create DiGraph of quests. nodes have questline and locations(?) as attributes. edges go FROM a prereq quest TO subsequent quest. this graph will NOT be complete.
    #   3(a). save quests as objects to make processing edges easier later? include quest weight (mostly for radiant quests), prereq locations, and quest locations
    #   3(b). locations that appear in both a quest and its prereq may unfairly add weight to that location? investigate avg num of locations per quest
    #   3(c). might want finite list of quests (not including every radiant variation) for later reference

    # 4. create graph of quest-location connections, weight on edges represents how many times this connection appears in the quests

if __name__ == "__main__":
    main()