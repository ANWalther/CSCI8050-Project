import networkx as nx
import csv
import math
import QuestData as quests

locations_data_file = "data/skyrim-locations.csv"
location_proximity_limit = 19800 # arbitrarily chosen value based on distance b/w Whiterun and Western Watchtower

def CreateQuestlinesGraph(quest_list:list[quests.Quest]) -> nx.DiGraph:
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

def ReadLocations(proximity_edges:bool=False) -> nx.Graph:
    locations_graph = nx.Graph()
    with open(locations_data_file, 'r') as locations_data:
        locations = csv.DictReader(locations_data)
        for location in locations:
            name = location['LOCATION_NAME']
            x = float(location['X_COORD'])
            y = float(location['Y_COORD'])
            locations_graph.add_node(name, hold=location['HOLD'], x_coord=x, y_coord=y)
            if proximity_edges:
                AddLocationProximityEdges(locations_graph, name)
    
    return locations_graph

def AddLocationProximityEdges(locations_graph:nx.Graph, nodeA:str):
    x_coords = nx.get_node_attributes(locations_graph, "x_coord", default=None)
    y_coords = nx.get_node_attributes(locations_graph, "y_coord", default=None)
    
    for nodeB in locations_graph.nodes:
        if not nodeA == nodeB:
            xA = x_coords[nodeA]
            yA = y_coords[nodeA]

            xB = x_coords[nodeB]
            yB = y_coords[nodeB]

            if math.dist([xA,yA], [xB,yB]) <= location_proximity_limit:
                locations_graph.add_edge(nodeA, nodeB, weight=1)

def AddEdge(locations_graph:nx.Graph, locations:tuple[str,str], edge_weight:float):
    locationA = locations[0]
    locationB = locations[1]
    if locations_graph.has_edge(locationA, locationB):
        w = locations_graph[locationA][locationB]["weight"]
        locations_graph.add_edge(locationA, locationB, weight=(edge_weight+w))
    else:
        locations_graph.add_edge(locationA, locationB, weight=edge_weight)

def GetLocationPairs(locationsA:list[str], locationsB:list[str]=None) -> list[tuple[str, str]]:
    # Note to self: can't overload functions bc Python
    pairs = []

    if locationsB == None:
        locs = locationsA.copy()
        while len(locs) > 1:
            locA = locs.pop(0)
            for locB in locs:
                pairs.append((locA, locB))

    else:                
        for locA in locationsA:
            for locB in locationsB:
                if not locA == locB:
                    pairs.append((locA, locB))

    return pairs

def UpdateQuestLocationsGraph(quest_list:list[quests.Quest], locations_graph:nx.Graph):

    # loop through quest list
    for quest in quest_list:
        # add edges between locations in quest
        for pair in GetLocationPairs(quest.locations):
            AddEdge(locations_graph, pair, quest.quest_weight)

        # add edges between locations in quest w/ locations in prereq quest
        for prereq in quests.GetPrereqQuests(quest_list, quest):
            for pair in GetLocationPairs(prereq.locations, quest.locations):
                AddEdge(locations_graph, pair, quest.quest_weight)

def CreateQuestGraph(filter:str=None, proximity:bool=False) -> nx.Graph:
    graph = ReadLocations(proximity)
    quest_list = quests.ReadQuests(filter)
    UpdateQuestLocationsGraph(quest_list, graph)

    return graph

def main():

    print("Reading locations data")
    locationGraph = ReadLocations()
    print("Locations data finished\n")
    #print(locationGraph.nodes(True))

    print("Reading quests data")
    questsData = quests.ReadQuests()
    print("Quests data finished\n")
    #for q in questsData:
        #print(q)

    print("Create questlines graph")
    #questlineGraph = CreateQuestlinesGraph(questsData)
    print("Questlines graph finished")
    #print(questlineGraph.edges)

    print("Create quest locations graph")
    UpdateQuestLocationsGraph(questsData, locationGraph)
    print("Quest locations graph finished")
    #print(questLocationsGraph.edges(data=True))

    # 3. for interest reasons, create DiGraph of quests. nodes have questline and locations(?) as attributes. edges go FROM a prereq quest TO subsequent quest.
    #   3(a). save quests as objects to make processing edges easier later? include quest weight (mostly for radiant quests), prereq locations, and quest locations
    #   3(b). locations that appear in both a quest and its prereq may unfairly add weight to that location? investigate avg num of locations per quest
    #   3(c). might want finite list of quests (not including every radiant variation) for later reference

    # 4. create graph of quest-location connections, weight on edges represents how many times this connection appears in the quests

if __name__ == "__main__":
    main()