import csv
import os
import datetime as dt

quests_data_file = "data/skyrim-quests.csv"

class Quest:
    def __init__(self, name:str, questline:str, prerequisites:str, locations:str):
        self.name = name
        self.questline = questline
        self.locations = [x.strip() for x in locations.split(".")]

        if prerequisites.lower() == "none":
            self.prerequisites = []
        else:
            self.prerequisites = [x.strip() for x in prerequisites.split(".")]

        if "RADIANT" in name.upper():
            num = name.split("/")[1] # remove everything before and including the forawrd slash
            num = num.split(")")[0] # remove everything after the close parenthesis (just in case Radiant marker is not last part of quest name)
            self.quest_weight = 1/float(num)
        else:
            self.quest_weight = 1
    
    def __str__(self):
        return "{" + self.name + ", " + self.questline + ", " + str(self.prerequisites) + ", " + str(self.locations) + ", " + str(self.quest_weight) + "}"

def ReadQuests(questline_filter:str=None) -> list[Quest]:
    quest_list = []
    with open(quests_data_file, 'r') as quests_data:
        quests = csv.DictReader(quests_data)
        for quest in quests:
            name = quest['QUEST_NAME']
            line = quest['QUESTLINE']
            prereq = quest['PREREQUISITE_QUEST']
            locations = quest['LOCATIONS']
            if questline_filter == None or questline_filter == line:
                quest_list.append(Quest(name, line, prereq,locations))
    
    return quest_list

def GetPrereqQuests(quest_list:list[Quest], quest:Quest) -> list[Quest]:
    prereqs = []

    for pq_name in quest.prerequisites:
        pq = next((x for x in quest_list if x.name == pq_name), None)
        if not pq == None:
            prereqs.append(pq)
    
    return prereqs

def RemoveRadiantQuestVariants(quest_list:list[Quest]) -> tuple[list[Quest], list[Quest]]:
    ret_quests = []
    radiant_quests = []
    for quest in quest_list:
        if not "RADIANT" in quest.name.upper():
            ret_quests.append(quest)
        else:
            radiant_quests.append(quest)

    return ret_quests, radiant_quests

def main():

    # Generate basic data analysis of quest data
    print("Quest Analytics")
    quest_list, radiant_quests = RemoveRadiantQuestVariants(ReadQuests())

    avg_locs = 0
    loc_counts = {}
    questline_counts = {}
    for quest in quest_list:
        avg_locs += len(quest.locations)

        if quest.questline in questline_counts:
            questline_counts[quest.questline] += 1
        else:
            questline_counts[quest.questline] = 1

        for loc in quest.locations:
            if loc in loc_counts:
                loc_counts[loc] += 1
            else:
                loc_counts[loc] = 1

    avg_locs = avg_locs/len(quest_list)

    with open(os.path.join(os.getcwd(), "output", "basic_quest_analytics.txt"), 'w') as report_file:
        report_file.write(f"Report Generated {dt.datetime.now()}\n\n")
        report_file.write(f"Number of quests         : {len(quest_list)}\n")
        report_file.write(f"Number of locations      : {len(loc_counts)}\n")
        report_file.write(f"AVG locations per quest  : {avg_locs}\n\n")
        report_file.write(f"Quests per questline     :\n")
        for qline in sorted(questline_counts, key=questline_counts.get, reverse=True):
            report_file.write(f"{qline:<24} : {questline_counts[qline]}\n")

        report_file.write(f"\nLocation use counts           :\n")
        for loc in sorted(loc_counts, key=loc_counts.get, reverse=True):
            report_file.write(f"{loc:<29} : {loc_counts[loc]}\n")

    print(f"Report exported, check output/basic_quest_analytics.txt")


if __name__ == "__main__":
    main()