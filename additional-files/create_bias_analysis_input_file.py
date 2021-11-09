import pandas as pd 
import csv

# This file creates a text file for use in the bias (sentiment + regard) classification
# Currently, it only supports ConceptNet (where relations are already in NL)

# global variables 
DATA_PATH = '/nas/home/malte/ckids-comet-atomic-2020/data/'
DATA_OUTPUT_PATH = '/nas/home/malte/ckids-comet-atomic-2020/nlg-bias/data/'
COMET_OUTPUT_FILE_NAME = 'conceptnet_comet_output_file.tsv'
KG = 'conceptnet'

# read predictions as dataframe
def get_predictions(file_name):
    return pd.read_csv(file_name, names = ['head_event', 'relation', 'tail_event'], encoding='latin-1', sep="\t")

# write unmasked version of comet predictions
def get_unmasked_version(keyword, relation, tail):
    if pd.isna(tail):
        tail = ''
    return keyword.lower() + '\t' + relation.lower() + '\t' + tail.lower().strip()

# write masked version of comet predictions
def get_masked_version(relation, tail):
    if pd.isna(tail):
        tail = ''
    return 'this person' + '\t' + relation.lower() + '\t' + tail.lower().strip()

# creates conditions on which a particular line should be skipped
def should_skip_line(keyword, relation, tail):
    if relation == 'defined as':
        return True
    return False

if __name__ == '__main__':

    preds = get_predictions(DATA_PATH + COMET_OUTPUT_FILE_NAME)

    with open(DATA_OUTPUT_PATH + KG + '_bias_input.txt', 'w+') as bias_input_file:
        for index, row in preds.iterrows():
            keyword = row['head_event']
            relation = row['relation']
            tail = row['tail_event']

            if should_skip_line(keyword, relation, tail) == False:
                if index != 0:
                    bias_input_file.write('\n')
                bias_input_file.write(get_unmasked_version(keyword, relation, tail))
                bias_input_file.write('\n')
                bias_input_file.write(get_masked_version(relation, tail))