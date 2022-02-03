import pandas as pd
import csv

# This file maps output from Comet into NL to be used in regard + sentiment classifiers

# set KG from which to use relations
KG = 'conceptnet'
# KG = 'atomic'
# KG = 'wikidata'
MODEL_SIZE = "t5base"
OUTPUT_FILE_PATH = "/nas/home/malte/ckids-comet-atomic-2020/data/"
INPUT_FILE = "/nas/home/malte/ckids-comet-atomic-2020/data/conceptnet_comet_t5base_output.tsv"

# read predictions as dataframe
def get_predictions(file_path):
    return pd.read_csv(file_path, names = ['head_event', 'relation', 'tail_event'], encoding='latin-1', sep="\t")

# use same mapping as corresponding relations in ConceptNet
def get_wikidata_mapping():
    return {'/r/IsA': 'is a ',
    '/r/RelatedTo': 'is related to ',
    '/r/UsedFor': 'is used for ',
    '/r/PartOf': 'is part of ',
    '/r/MadeOf': 'is made of ',
    '/r/HasProperty': 'has the property ',
    '/r/Causes': 'causes ',
    '/r/CreatedBy': 'is created by ',
    '/r/HasPrerequisite': 'requires '
    }

# relations are taken from intersection of Filip's file and Nina's relations
# NL mappings are taken from Nina's mapping
def get_conceptnet_mapping():
    return {'at location': 'is located at',
    'capable of': 'is capable of',
    'causes': 'causes',
    'causes desire': 'causes the desire to',
    'created by': 'is created by',
    'defined as': 'is defined as',
    'desires': 'desires',
    'has a': 'has a',
    'has first subevent': 'starts with',
    'has last subevent': 'ends with',
    'has prerequisite': 'requires',
    'has property': 'has the property',
    'has subevent': 'requires',
    'instance of': 'is an instance of',
    'is a': 'is a',
    'located near': 'is located near',
    'made of': 'is made of', 
    'motivated by goal': 'is motivated by',
    'not capable of': 'is not capable of',
    'not desires': 'does not desire',
    'not has property': 'does not have the property',
    'part of': 'is part of',
    'receives action': 'receives action of',
    'related to': 'is related to',
    'symbol of': 'is a symbol of',
    'used for': 'is used for'}

# these relations and NL equivalents are taken from Nina's work
def get_conceptnet_mapping_old():
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

if __name__ == '__main__':

    # read in predictions as dataframe
    full_pred = get_predictions(INPUT_FILE)

    # obtain appropriate mapping of relation to NL
    if KG == 'conceptnet':
        mapping = get_conceptnet_mapping()
    elif KG == 'wikidata':
        mapping = get_wikidata_mapping()

    # write NL sentences to file
    with open(OUTPUT_FILE_PATH + KG + '_comet_' + MODEL_SIZE +'_nl_output.tsv', 'w+') as outfile:
        tsv_writer = csv.writer(outfile, delimiter="\t")
        for index, row in full_pred.iterrows():
            relation_to_text = mapping[row['relation']]
            tsv_writer.writerow([row['head_event'], relation_to_text, row['tail_event']])