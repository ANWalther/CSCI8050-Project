import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as img
import CreateGraphs
import QuestData

hold_colors = {
    "Eastmarch" : "#ff3300", "Falkreath Hold" : "#ff9900", "Haafingar" : "#ffff66",
    "Hjaalmarch" : "#33cc33", "The Pale" : "#00ffff", "The Reach" : "#0066ff",
    "The Rift" : "#9966ff", "Whiterun Hold" : "#669999", "Winterhold" : "#666699"
}

def GetNodeDrawData(locations_graph:nx.Graph):
    node_pos = {}
    node_col = {}

    x_coords = nx.get_node_attributes(locations_graph, "x_coord", default=None)
    y_coords = nx.get_node_attributes(locations_graph, "y_coord", default=None)
    holds = nx.get_node_attributes(locations_graph, "hold")

    for node in locations_graph.nodes:
        if not node in x_coords or not node in y_coords or x_coords[node] == None or y_coords[node] == None:
            print(node)
            continue
        x = x_coords[node]
        y = y_coords[node]
        node_pos[node] = (x,y)
        node_col[node] = hold_colors[holds[node]]
        
    
    #node_pos = nx.rescale_layout_dict(node_pos, graph_scale)    
    return node_pos, node_col
    

def DrawQuestlinesGraph(questlines_graph:nx.DiGraph):
    # First generate layout
    
    nx.draw_networkx(questlines_graph)
    plt.show()
    return

def DrawLocationsGraph(locations_graph:nx.Graph):
    # draw edges then nodes and edge labels for more fine-tuned control
    #nx.draw_networkx(locations_graph, pos=GetLocationsPositions(locations_graph))

    node_pos, node_col = GetNodeDrawData(locations_graph)
    overworld_subgraph = nx.induced_subgraph(locations_graph, node_pos.keys())
    #nx.draw_networkx_edges(overworld_subgraph, pos=node_pos, node_size=10)
    nx.draw_networkx_nodes(overworld_subgraph, pos=node_pos, node_color=node_col.values(), node_size=100)
    nx.draw_networkx_labels(overworld_subgraph, pos=node_pos, font_size=10)
    plt.show()
    return

def main():
    # create graphs using CreateGraphs

    # NOTE: to use coordinates for locations, this information MUST be stored in a dictionary with node keys and position values
    #       Additionally, may want to exclude locations WITHOUT coordinates from an overworld representation of locations
    
    print("Draw Graphs Main")

    quest_data = QuestData.ReadQuests()
    locations_graph = CreateGraphs.ReadLocations(False)
    CreateGraphs.UpdateQuestLocationsGraph(quest_data, locations_graph)

    DrawLocationsGraph(locations_graph)

    # Test drawing locations graph with quest edges
    #questData = CreateGraphs.ReadQuests()
    #quest_loc_graph = CreateGraphs.CreateQuestLocationsGraph(questData, locations_graph)
    #DrawLocationsGraph(quest_loc_graph)

    print("Draw Graphs Main End")

if __name__ == "__main__":
    main()