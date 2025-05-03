import networkx as nx
import CreateGraphs
import QuestData
import datetime as dt
import os

player_origin = "Helgen"

def ExportReport(filename:str, report:str):
    with open(os.path.join(os.getcwd(), "output/graphReports", filename), 'w') as report_file:
        report_file.write(f"Report Generated {dt.datetime.now()}\n\n")
        report_file.write(report)
    print(f"Report exported, check output/graphReports/{filename}")

def GenerateBasicReport(graph:nx.Graph) -> str:
    report = "Basic Analytics - player origin '{}' \n\n".format(player_origin)

    nontrivial_connected_components = []
    num_isolated_nodes = 0
    for c in nx.connected_components(graph):
        if len(c) > 1:
            nontrivial_connected_components.append(c)
        else:
            num_isolated_nodes += 1

    # num of nodes, edges, graph density, connected components
    report += "{} nodes, {} edges\ngraph density {}\n{} isolated node(s) ({:.2f}% isolated)\n".format(graph.number_of_nodes(), 
                                                                                         graph.number_of_edges(), 
                                                                                         nx.density(graph),
                                                                                         num_isolated_nodes,
                                                                                         (float(num_isolated_nodes)/graph.number_of_nodes())*100)
    
    report += "{} nontrivial connected component(s)\nnontrivial component size(s): ".format(len(nontrivial_connected_components))
    for c in nontrivial_connected_components:
        report += "{} ".format(len(c))
    
    report += "\n\n"

    # node weights (sum of node edge-weights)
    node_weights = nx.degree(graph, weight="weight")
    report += "{:<30} : Weight\n".format("Locations")

    for node in sorted(node_weights, key=lambda x : x[1], reverse=True):
        report += "{:<30} : {:.1f}\n".format(node[0], node[1])

    return report

def GenerateStochasticReport(graph:nx.Graph) -> str:
    report = "Stochastic Columm Sums\n\n"

    stoch_matrix = GenerateStochasticMatrix(graph)
    col_sums = {}

    for nodeRow in graph.nodes:
        for nodeCol in graph.nodes:
            if not nodeCol in stoch_matrix[nodeRow]:
                continue

            if nodeCol in col_sums:
                col_sums[nodeCol] += stoch_matrix[nodeRow][nodeCol]
            else:
                col_sums[nodeCol] = stoch_matrix[nodeRow][nodeCol]

    # large column sum means the location is important in its connected subgraph
    for node in sorted(col_sums, key=col_sums.get, reverse=True):
        report += "{:<30} : {:.2f}\n".format(node, col_sums[node])

    return report

def GenerateStochasticMatrix(graph:nx.graph):
    adj_matrix = nx.to_dict_of_dicts(graph)
    node_weights = nx.degree(graph, weight="weight")
    stoch_matrix = {}

    for nodeRow in graph.nodes:
        stoch_matrix[nodeRow] = {}
        for nodeCol in graph.nodes:
            if not nodeCol in adj_matrix[nodeRow]:
                #stoch_matrix[nodeRow][nodeCol] = 0
                continue
            
            prob = adj_matrix[nodeRow][nodeCol]['weight'] / node_weights[nodeRow]
            stoch_matrix[nodeRow][nodeCol] = prob
    
    return stoch_matrix

def main():
    print("Analyze Graphs Main")

    quest_data = QuestData.ReadQuests()
    prox_graph = CreateGraphs.ReadLocations(True)
    ExportReport("basic_proximity_analytics.txt", GenerateBasicReport(prox_graph))
    ExportReport("stochastic_proximity_analytics.txt", GenerateStochasticReport(prox_graph))

    quests_graph = CreateGraphs.ReadLocations(False)
    CreateGraphs.UpdateQuestLocationsGraph(quest_data, quests_graph)
    ExportReport("basic_quests_analytics.txt", GenerateBasicReport(quests_graph))
    ExportReport("stochastic_quests_analytics.txt", GenerateStochasticReport(quests_graph))

    CreateGraphs.UpdateQuestLocationsGraph(quest_data, prox_graph)
    ExportReport("basic_quests_and_proximity_analytics.txt", GenerateBasicReport(prox_graph))
    ExportReport("stochastic_quests_and_proximity_analytics.txt", GenerateStochasticReport(prox_graph))

    main_quest_data = QuestData.ReadQuests(questline_filter="Main Quest")
    main_quest_graph = CreateGraphs.ReadLocations(False)
    CreateGraphs.UpdateQuestLocationsGraph(main_quest_data, main_quest_graph)
    ExportReport("basic_main_quest_analytics.txt", GenerateBasicReport(main_quest_graph))
    ExportReport("stochastic_main_quest_analytics.txt", GenerateStochasticReport(main_quest_graph))

    main_quest_prox_graph = CreateGraphs.ReadLocations(True)
    CreateGraphs.UpdateQuestLocationsGraph(main_quest_data, main_quest_prox_graph)
    ExportReport("basic_main_quest_and_prox_analytics.txt", GenerateBasicReport(main_quest_prox_graph))
    ExportReport("stochastic_main_quest_and_prox_analytics.txt", GenerateStochasticReport(main_quest_prox_graph))

    side_quest_data = QuestData.ReadQuests(questline_filter="Side Quest")
    side_quest_graph = CreateGraphs.ReadLocations(False)
    CreateGraphs.UpdateQuestLocationsGraph(side_quest_data, side_quest_graph)
    ExportReport("basic_side_quest_analytics.txt", GenerateBasicReport(side_quest_graph))
    ExportReport("stochastic_side_quest_analytics.txt", GenerateStochasticReport(side_quest_graph))
    
    

if __name__ == "__main__":
    main()