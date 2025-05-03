import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as img
import CreateGraphs
import QuestData

hold_colors = {
    "Eastmarch" : "#ff3300", "Falkreath Hold" : "#ff9900", "Haafingar" : "#ffff66",
    "Hjaalmarch" : "#33cc33", "The Pale" : "#00ffff", "The Reach" : "#0066ff",
    "The Rift" : "#9966ff", "Whiterun Hold" : "#669999", "Winterhold" : "#666699", "" : "#990099"
}

def GetNodeDrawData(graph:nx.Graph):
    node_pos = {}
    node_col = {}

    x_coords = nx.get_node_attributes(graph, "x_coord", default=None)
    y_coords = nx.get_node_attributes(graph, "y_coord", default=None)
    holds = nx.get_node_attributes(graph, "hold", default="")

    spareX = -150000
    spareY = 150000
    for node in graph.nodes:
        if not node in x_coords or not node in y_coords or x_coords[node] == None or y_coords[node] == None:
            node_pos[node] = (spareX,spareY)
            node_col[node] = "#990099"
            spareX += 50000
            continue
        x = x_coords[node]
        y = y_coords[node]
        node_pos[node] = (x,y)
        node_col[node] = hold_colors[holds[node]]
        
    
    #node_pos = nx.rescale_layout_dict(node_pos, graph_scale)    
    return node_pos, node_col

def GetEdgeDrawData(graph:nx.Graph):
    edge_weights = nx.get_edge_attributes(graph, "weight", default=0)
    edge_widths = []
    max_weight = float(max(list(edge_weights.values())))

    #edge widths scaled by weight
    for edge in edge_weights:
        weight = edge_weights[edge]
        edge_widths.append((weight/max_weight)*2)
    
    return edge_widths

    

def DrawQuestlinesGraph(graph:nx.DiGraph):
    # First generate layout
    
    nx.draw_networkx(graph)
    plt.show()
    return

def DrawLocationsGraph(graph:nx.Graph, filename:str=None, scale_edges:bool=False, img_dpi=1500):
    # draw edges then nodes and edge labels for more fine-tuned control
    #nx.draw_networkx(locations_graph, pos=GetLocationsPositions(locations_graph))

    node_pos, node_col = GetNodeDrawData(graph)
    #overworld_subgraph = nx.induced_subgraph(graph, node_pos.keys())
    edge_widths = GetEdgeDrawData(graph) if scale_edges else 0.5
    nx.draw_networkx_edges(graph, pos=node_pos, node_size=1, width=edge_widths)
    nx.draw_networkx_nodes(graph, pos=node_pos, node_color=node_col.values(), node_size=8)
    nx.draw_networkx_labels(graph, pos=node_pos, font_size=2, font_color="#595959", font_weight="bold", font_family="monospace")
    if not filename == None:
        plt.savefig(filename, format="png", dpi=img_dpi, pad_inches=0.01)

    plt.show()
    return

def main():
    # create graphs using CreateGraphs

    # NOTE: to use coordinates for locations, this information MUST be stored in a dictionary with node keys and position values
    #       Additionally, may want to exclude locations WITHOUT coordinates from an overworld representation of locations
    
    print("Draw Graphs Main")

    quest_data = QuestData.ReadQuests()
    locations_prox_graph = CreateGraphs.ReadLocations(True)
    DrawLocationsGraph(locations_prox_graph, "output/locations_proximity.png")

    quests_graph = CreateGraphs.ReadLocations(False)
    CreateGraphs.UpdateQuestLocationsGraph(quest_data, quests_graph)
    DrawLocationsGraph(quests_graph, filename="output/locations_quests.png", scale_edges=False)

    CreateGraphs.UpdateQuestLocationsGraph(quest_data, locations_prox_graph)
    DrawLocationsGraph(locations_prox_graph, filename="output/locations_quests_and_proximity.png", scale_edges=False)

    main_quest_data = QuestData.ReadQuests(questline_filter="Main Quest")
    main_quest_graph = CreateGraphs.ReadLocations(False)
    CreateGraphs.UpdateQuestLocationsGraph(main_quest_data, main_quest_graph)
    DrawLocationsGraph(main_quest_graph, filename="output/locations_main_quest.png", scale_edges=True)
    

    # Test drawing locations graph with quest edges
    #questData = CreateGraphs.ReadQuests()
    #quest_loc_graph = CreateGraphs.CreateQuestLocationsGraph(questData, locations_graph)
    #DrawLocationsGraph(quest_loc_graph)

    print("Draw Graphs Main End")

if __name__ == "__main__":
    main()