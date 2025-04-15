import networkx as nx

def main():
    # Steps to making graphs:

    # 1. read locations data into nodes with the hold, x coord, and y coord as node attributes. we'll keep this as a secondary graph for now with no edges

    # 2. read quest data, however some quests use other quests as prerequisites, and their order is not guaranteed.
    #    to account for this, first put all quests into a queue for processing. If a quest's prerequisite hasn't been processed, throw it to the end of the queue
    #    if the quest is reached in the queue a second time and the prerequisite still hasn't been processed, discard it as bad data

    # 3. for interest reasons, create DiGraph of quests. nodes have questline and locations(?) as attributes. edges go FROM a prereq quest TO subsequent quest. this graph will NOT be complete.
    #   3(a). save quests as objects to make processing edges easier later? include quest weight (mostly for radiant quests), prereq locations, and quest locations
    #   3(b). locations that appear in both a quest and its prereq may unfairly add weight to that location? investigate avg num of locations per quest
    #   3(c). might want finite list of quests (not including every radiant variation) for later reference

    # 4. create graph of quest-location connections, weight on edges represents how many times this connection appears in the quests
    
    print("main")

if __name__ == "__main__":
    main()