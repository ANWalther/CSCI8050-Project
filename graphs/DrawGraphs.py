import networkx as nx
import matplotlib.pyplot as plt
import CreateGraphs

graph_scale = 10.0

def DrawQuestlinesGraph(questlines_graph:nx.DiGraph):
    # First generate layout
    
    nx.draw_networkx(questlines_graph)
    plt.show()
    return

def DrawLocationsGraph(locations_graph:nx.Graph):
    node_pos = {}
    x_coords = nx.get_node_attributes(locations_graph, "x_coord", default=0)
    y_coords = nx.get_node_attributes(locations_graph, "y_coord", default=0)

    for node in locations_graph.nodes:
        x = x_coords[node]
        y = y_coords[node]
        node_pos[node] = (x,y)
        if x == y and x == 0:
            print(node)

    #node_pos = nx.rescale_layout_dict(node_pos, graph_scale)
    nx.draw_networkx(locations_graph, pos=node_pos)
    plt.show()
    return

def main():
    # create graphs using CreateGraphs

    # NOTE: to use coordinates for locations, this information MUST be stored in a dictionary with node keys and position values
    #       Additionally, may want to exclude locations WITHOUT coordinates from an overworld representation of locations
    
    print("Draw Graphs Main")

    # Test drawing questlines graph
    #print("Draw Questlines Graph")
    #questData = CreateGraphs.ReadQuests()
    #questlines_graph = CreateGraphs.CreateQuestlinesGraph(questData)

    # DrawQuestlinesGraph(questlines_graph)

    # Test drawing locations graph
    locations_graph = CreateGraphs.ReadLocations()
    #DrawLocationsGraph(locations_graph)

    # Test drawing locations graph with quest edges
    questData = CreateGraphs.ReadQuests()
    quest_loc_graph = CreateGraphs.CreateQuestLocationsGraph(questData, locations_graph)
    DrawLocationsGraph(quest_loc_graph)

    print("Draw Graphs Main End")

if __name__ == "__main__":
    main()