import pandas as pd

# NOTE: updates happen in T5 branch. As of 11/3, this might no longer be up to date.

# This file maps output from Comet into NL to be used in regard + sentiment classifiers

# set KG from which to use relations
KG = 'conceptnet'
# KG = 'atomic'
# KG = 'wikidata'

# read predictions as dataframe
def get_predictions(file_name):
    return pd.read_csv(file_name, names = ['head_event', 'relation', 'tail_event'], encoding='latin-1', sep="\t")

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

# these relations and NL equivalents are taken from Nina's work
def get_conceptnet_mapping():
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
    full_pred = get_predictions('test.tsv')

    # obtain appropriate mapping of relation to NL
    if KG == 'conceptnet':
        mapping = get_conceptnet_mapping()
    elif KG == 'wikidata':
        mapping = get_wikidata_mapping()

    # write NL sentences to file
    with open('./' + KG + '_comet_NL_output.txt', 'w+') as outfile:
        for index, row in full_pred.iterrows():
            relation_to_text = mapping[row['relation']]
            outfile.write(row['head_event'] + ' ' + relation_to_text + row['tail_event'] + '\n')