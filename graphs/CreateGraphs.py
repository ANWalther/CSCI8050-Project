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

        if "RADIANT" in name.upper():
            num = name.split("/")[1] # remove everything before and including the forawrd slash
            num = num.split(")")[0] # remove everything after the close parenthesis (just in case Radiant marker is not last part of quest name)
            self.quest_weight = 1/float(num)
        else:
            self.quest_weight = 1
    
    def __str__(self):
        return "{" + self.name + ", " + self.questline + ", " + str(self.prerequisites) + ", " + str(self.locations) + ", " + str(self.quest_weight) + "}"

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

def CreateQuestlinesGraph(quest_list:list[Quest]):
    questlines_graph = nx.DiGraph()
    #   first put all quests into a queue for processing. If a quest's prerequisite hasn't been processed check if that prereq exists layer in the queue
    #    if the prereq exists, throw it to the end of the queue. otherwise discard the quest as bad data.

    quest_queue = quest_list.copy()

    while len(quest_queue):
        quest = quest_queue.pop(0) # dequeue
        
        # if any prerequisite quests are not in the graph, enque quest and move on
        if any(pq not in questlines_graph for pq in quest.prerequisites):
            # if all prerequisite quest exists in either the queue or the graph,
            # enqueue quest to be processed later
            if all((pq in questlines_graph or any(pq == q.name for q in quest_queue)) for pq in quest.prerequisites):
                quest_queue.append(quest) # enqueue
            # else quest is discarded as bad data
            continue

        # add quest to graph
        questlines_graph.add_node(quest.name, questline=quest.questline)

        # add edges from any and all prerequisite quests to this quest
        for prereq in quest.prerequisites:
            questlines_graph.add_edge(prereq, quest.name)

    return questlines_graph 

def CreateQuestLocationsGraph(quest_list:list[Quest], locations_graph:nx.Graph):
    quest_locations_graph = nx.Graph(locations_graph.nodes)

    return quest_locations_graph

def main():

    print("Reading locations data")
    locationGraph = ReadLocations()
    print("Locations data finished\n")
    #print(locationGraph.nodes(True))

    print("Reading quests data")
    questsData = ReadQuests()
    print("Quests data finished\n")
    #for q in questsData:
        #print(q)

    print("Create questlines graph")
    questlineGraph = CreateQuestlinesGraph(questsData)
    print("Questlines graph finished")
    ExportQuestlinesGraph(questlineGraph, "output/questlines-graph.txt")
    print("Questlines graph exported - chech output/questlines-graph.txt\n")
    #print(questlineGraph.edges)


    # 3. for interest reasons, create DiGraph of quests. nodes have questline and locations(?) as attributes. edges go FROM a prereq quest TO subsequent quest.
    #   3(a). save quests as objects to make processing edges easier later? include quest weight (mostly for radiant quests), prereq locations, and quest locations
    #   3(b). locations that appear in both a quest and its prereq may unfairly add weight to that location? investigate avg num of locations per quest
    #   3(c). might want finite list of quests (not including every radiant variation) for later reference

    # 4. create graph of quest-location connections, weight on edges represents how many times this connection appears in the quests

if __name__ == "__main__":
    main()