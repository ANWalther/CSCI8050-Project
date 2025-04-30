import networkx as nx
import CreateGraphs
import datetime as dt
import os

player_origin = "Helgen"

def ExportReport(filename:str, report:str):
    with open(os.path.join(os.getcwd(), "output", filename), 'w') as report_file:
        report_file.write(f"{dt.datetime.now()}\n")
        report_file.write(report)
    print(f"Report exported, check output/{filename}")

def GenerateBasicReport(graph:nx.Graph) -> str:
    report = "Basic Analytics\n\n"

    # num of nodes
    # graph density
    # degree histogram - highest and lowest weight nodes (5 of each?)
    # degree centrality of origin
    # dispersion centrality of origin

    return report

def GenerateCommunicabilityReport(graph:nx.Graph) -> str:
    report = "Communicability Analytics\n\n"

    # communicability - write as a matrix

    return report

def main():
    print("Analyze Graphs Main")

    # Metrics to include in analysis:
    # 

if __name__ == "__main__":
    main()