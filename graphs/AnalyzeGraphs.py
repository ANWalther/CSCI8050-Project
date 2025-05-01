import networkx as nx
import CreateGraphs
import QuestData
import datetime as dt
import os

player_origin = "Helgen"

def ExportReport(filename:str, report:str):
    with open(os.path.join(os.getcwd(), "output", filename), 'w') as report_file:
        report_file.write(f"Report Generated {dt.datetime.now()}\n\n")
        report_file.write(report)
    print(f"Report exported, check output/{filename}")

def GenerateBasicReport(graph:nx.Graph) -> str:
    report = "Basic Analytics - player origin '{}' \n\n".format(player_origin)

    # num of nodes, edges, and graph density
    report += "{} nodes, {} edges\ngraph density {}\n\n".format(graph.number_of_nodes(), graph.number_of_edges(), nx.density(graph))

    # node weights (sum of node edge-weights)
    node_weights = nx.degree(graph, weight="weight")
    report += "{:<30} : Weight\n".format("Locations")

    for node in sorted(node_weights, key=lambda x : x[1], reverse=True):
        report += "{:<30} : {:.1f}\n".format(node[0], node[1])

    return report

def GenerateCommunicabilityReport(graph:nx.Graph) -> str:
    report = "Communicability Analytics\n\n"

    # communicability - write as a matrix

    return report

def main():
    print("Analyze Graphs Main")

    loc_graph = CreateGraphs.ReadLocations(proximity_edges=True)
    quest_list = QuestData.ReadQuests()
    CreateGraphs.UpdateQuestLocationsGraph(quest_list, loc_graph)
    
    ExportReport("basic_quest_location_graph_analytics.txt", GenerateBasicReport(loc_graph))

if __name__ == "__main__":
    main()