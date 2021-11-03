import pandas as pd
import csv

# This file compares the relations present in WikiData-CS and ConceptNet

def get_data(file_name):
    # encoding='latin-1', 
    return pd.read_csv(file_name, names = ['node1', 'relation', 'node2', 'node1;label', 'node2;label', 'relation;label', 'relation;dimension', 'source', 'sentence'], sep="\t")

def get_conceptnet_relations_to_text():
    return {'DefinedAs': 'is defined as ',
    'DesireOf': 'desires ',
    'HasA': 'has a ',
    'HasFirstSubevent': 'starts with ',
    'HasLastSubevent': 'ends with ',
    'HasPrerequisite': 'requires ',
    'HasProperty': 'has the property ',
    'HasSubevent': 'requires ',
    'IsA': 'is a ',
    'MadeOf': 'is made of ',
    'MotivatedByGoal': 'is motivated by ',
    'NotCapableOf': 'is not capable of ',
    'NotDesires': 'does not desire ',
    'NotHasA': 'does not have a ',
    'NotHasProperty': 'does not have the property ',
    'NotIsA': 'is not a ',
    'NotMadeOf': 'is not made of ',
    'PartOf': 'is part of ',
    'RelatedTo': 'is related to ',
    'SymbolOf': 'is a symbol of ',
    'UsedFor': 'is used for ',
    'AtLocation': 'is located at ',
    'CapableOf': 'is capable of ',
    'Causes': 'causes ',
    'CausesDesire': 'causes the desire to ',
    'CreatedBy': 'is created by ',
    'Desires': 'desires ',
    'HasPainCharacter': 'has pain character of ',
    'HasPainIntensity': 'has pain intensity of ',
    'InheritsFrom': 'inherits from ',
    'InstanceOf': 'is an instance of ',
    'LocatedNear': 'is located near ',
    'LocationOfAction': 'has location of action at ',
    'ReceivesAction': 'receives action of '}

data = get_data('wikidata-cs.tsv')

unique_relations_wiki = list(data['relation'].unique())
unique_relations_wiki.pop(0) # remove 'relation' from the list
unique_relations_conceptnet = list(get_conceptnet_relations_to_text().keys())

for i in range(len(unique_relations_wiki)):
    old_string = unique_relations_wiki[i]
    unique_relations_wiki[i] = old_string.replace('/r/', '')

print("\nunique relations in WikiData:")
print(unique_relations_wiki)
print("length of unique relations in WikiData:", len(unique_relations_wiki))
print()
print("unique relations in ConceptNet:")
print(unique_relations_conceptnet)
print("length of unique relations in ConceptNet:", len(unique_relations_conceptnet))
print()

relations_in_wiki_not_conceptnet = list(set(unique_relations_wiki) - set(unique_relations_conceptnet))
relations_in_conceptnet_not_wiki = list(set(unique_relations_conceptnet) - set(unique_relations_wiki))

relations_in_wikidata_also_in_conceptnet = list()
for relation in unique_relations_wiki:
    if relation in unique_relations_conceptnet:
        relations_in_wikidata_also_in_conceptnet.append(relation)

print("relations in wikidata but not in conceptnet:")
print(relations_in_wiki_not_conceptnet)
print()
print("relations in conceptnet but not in wikidata:")
print(relations_in_conceptnet_not_wiki)
print()
print("relations in wikidata that are also in conceptnet")
print(relations_in_wikidata_also_in_conceptnet)
print("length:", len(relations_in_wikidata_also_in_conceptnet))
print()

