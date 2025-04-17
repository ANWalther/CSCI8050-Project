import networkx as nx
import matplotlib.pyplot as plt
import CreateGraphs

def DrawQuestlinesGraph(questlines_graph:nx.DiGraph):
    # First generate layout
    
    nx.draw_networkx(questlines_graph)
    plt.show()
    return

def main():
    # create graphs using CreateGraphs

    # NOTE: to use coordinates for locations, this information MUST be stored in a dictionary with node keys and position values
    #       Additionally, may want to exclude locations WITHOUT coordinates from an overworld representation of locations
    
    print("Draw Graphs Main")

    # Test drawing questlines graph
    print("Draw Questlines Graph")
    questData = CreateGraphs.ReadQuests()
    questlines_graph = CreateGraphs.CreateQuestlinesGraph(questData)

    DrawQuestlinesGraph(questlines_graph)

    print("Draw Graphs Main End")

if __name__ == "__main__":
    main()