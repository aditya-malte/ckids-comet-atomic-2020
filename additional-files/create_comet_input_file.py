import pandas as pd
import csv

# set KG from which to use relations
KG = 'conceptnet'
# KG = 'atomic'
# KG = 'wikidata'
DATA_PATH = "/nas/home/malte/ckids-comet-atomic-2020/data/"

def get_data(file_name):
    return pd.read_csv(DATA_PATH + file_name, names = ['head_event', 'relation', 'tail_event'], encoding='latin-1', sep="\t")

def get_keywords():
	return ['african_american','Armenian','Persian','American',
    'Filipino','English','Norwegian','Dutch','Israeli','Nigerian', 'Ethiopia', 
    'Europe', 'European', 'Russian', 'Ukraine',
    'Sudan', 'Afghanistan' ,'Iraq', 'Yemen', 'Ukrainian', 'Russia',
    'Italy', 'Somali', 'Iran', 'Afghan', 'Indian', 'Italian',
    'Australian', 'Spanish', 'Guatemalan', 'Hispanic', 'Venezuela', 'Sudanese',
    'Oman', 'Finnish', 'Swedish', 'Venezuelan', 'Puerto_Rican', 'Ghanaian',
    'Moroccan', 'Somalia', 'Saudi_Arabian', 'Syria', 'Chinese', 'Pakistani',
    'China', 'India', 'Irish', 'Britain', 'France', 'Greece',
    'Scotland', 'Mexican', 'Paraguayan', 'Brazil', 'African', 'Eritrean',
    'Sierra_Leonean', 'Africa', 'Jordan', 'Indonesia', 'Vietnam', 'Pakistan',
    'German', 'Romania' ,'Brazilian', 'Ecuadorian', 'Mexico', 'Puerto_Rico',
    'Kenyan', 'Liberian', 'Cameroonian', 'African_Americans', 'Kenya', 'Liberia',
    'Sierra_Leon', 'Qatari', 'Syrian', 'Arab', 'Saudi_Arabia', 'Lebanon',
    'Indonesian', 'French', 'Norwegian', 'South_Africa', 'Jordanian', 'Korea'
    ,'Singapore', 'Romanian', 'Crimean', 'Native_American', 'Germany', 'Ireland',
    'Ecuador', 'Morocco', 'Omani', 'Iranian', 'Iraqi', 'Qatar',
    'Turkey', 'Vietnamese', 'Nepali', 'Laos', 'Bangladesh', 'British',
    'Polish', 'Greek', 'Scottish', 'Bolivian', 'Guatemala', 'Ghana',
    'Cameroon', 'Japanese', 'Taiwanese','Bengali', 'Nepal', 'Albanian',
    'Albania', 'Columbian', 'Peruvian', 'Argentian', 'Spain', 'Paraguay',
    'Ethiopian', 'Egyptian', 'Persian_people', 'Sweden', 'Crimea', 'Portuguese',
    'Argentina', 'Chile', 'Cape_Verdean', 'Turkish', 'Yemeni', 'Taiwan',
    'Austrian', 'White_people', 'Finland', 'Australia', 'South_African', 'Eriteria',
    'Egypt', 'Korean', 'Dutch_people', 'Peru', 'Poland', 'Chilean',
    'Columbia', 'Bolivia', 'Laotian', 'Lebanese', 'Japan', 'Norway',
    'Cape_Verde', 'Portugal', 'Austria', 'Singaporean', 'Netherlands','she',
    'he','hers','him','her','herself', 'himself', 'his','woman','man','female',
    'male','lady','gentleman','ladies','gentlemen','girl','boy' ,'sir', 'ma_am',
    'mother','father','stepmother','stepfather','daughter', 'son','sister', 
    'brother',  'grandmother',   'grandfather' ,
    'mommy', 'daddy','wife','husband','bride', 'groom','girlfriend', 'boyfriend',
    'schoolgirl' , 'schoolboy','Sharia', 'Jihad', 'Christian', 'Muslim', 'Islam', 'Hindu',
    'Mohammed', 'church',  'Quran','Bible','Brahmin','Holy_Trinity','barber', 'coach', 
    'businessperson', 'football_player', 'construction_worker', 'manager',
    'CEO', 'accountant', 'commander', 'firefighter', 'mover', 'software_developer',
    'guard', 'baker', 'doctor', 'athlete', 'artist', 'dancer',
    'mathematician', 'janitor', 'carpenter', 'mechanic', 'actor', 'handyman',
    'musician', 'detective', 'politician', 'entrepreneur', 'model', 'opera_singer',
    'chief', 'lawyer', 'farmer', 'writer', 'librarian', 'army',
    'real_estate_developer', 'broker', 'scientist', 'butcher', 'electrician', 'prosecutor',
    'banker', 'cook', 'hairdresser', 'prisoner', 'plumber', 'attorney',
    'boxer', 'chess_player', 'priest', 'swimmer', 'tennis_player', 'supervisor',
    'attendant', 'housekeeper', 'maid', 'producer', 'researcher', 'midwife',
    'judge', 'umpire', 'bartender', 'economist', 'physicist', 'psychologist',
    'theologian', 'salesperson', 'physician', 'sheriff', 'cashier', 'assistant',
    'receptionist', 'editor', 'engineer', 'comedian', 'painter', 'civil_servant',
    'diplomat', 'guitarist', 'linguist', 'poet', 'laborer', 'teacher',
    'delivery_man', 'realtor', 'pilot', 'professor', 'chemist', 'historian',
    'pensioner', 'performing_artist', 'singer', 'secretary', 'auditor', 'counselor',
    'designer', 'soldier', 'journalist', 'dentist', 'analyst', 'nurse',
    'tailor', 'waiter', 'author', 'architect', 'academic', 'director',
    'illustrator', 'clerk', 'policeman', 'chef', 'photographer', 'drawer',
    'cleaner', 'pharmacist', 'pianist', 'composer', 'handball_player', 'sociologist']

# these relations are taken from Comet-2020
def get_atomic_relations():
    return ['oEffect', 'oReact', 'oWant', 'xAttr', 'xEffect', 'xIntent', 'xNeed', 'xReact', 'xWant', 
    'AtLocation', 'ObjectUse', 'Desires', 'HasProperty', 'NotDesires', 'Causes', 'HasSubEvent', 
    'xReason', 'CapableOf', 'MadeUpOf', 'isAfter', 'isBefore', 'isFilledBy', 'HinderedBy']

# these relations are taken from the relation;label column in the file Filip shared (kgtk_conceptnet.tsv)
def get_conceptnet_relations():
    return ['antonym', 'at location', 'capable of', 'causes', 'causes desire', 'created by', 'defined as', 
    'derived from', 'desires', 'distinct from', 'entails', 'etymologically derived from', 
    'etymologically related to', 'form of', 'has a', 'has context', 'has first subevent', 'has last subevent', 
    'has prerequisite', 'has property', 'has subevent', 'instance of', 'is a', 'located near', 'made of', 
    'manner of', 'motivated by goal', 'not capable of', 'not desires', 'not has property', 'part of', 'receives action', 
    'related to', 'similar to', 'symbol of', 'synonym', 'used for', 'capital', 'field', 'genre', 'genus', 
    'influenced by', 'known for', 'language', 'leader', 'occupation', 'product']

# these relations are taken from the relation;label column in the file Filip shared (kgtk_conceptnet.tsv)
# but, only include those that are also present in Nina's set
def get_conceptnet_relations_filtered():
    return ['at location', 'capable of', 'causes', 'causes desire', 'created by', 'defined as', 
    'desires', 'has a', 'has first subevent', 'has last subevent', 
    'has prerequisite', 'has property', 'has subevent', 'instance of', 'is a', 'located near', 'made of', 
    'motivated by goal', 'not capable of', 'not desires', 'not has property', 'part of', 'receives action', 
    'related to', 'symbol of', 'used for']

# relations are taken from intersection of Filip's file and Nina's relations
# NL mappings are taken from Nina's mapping
def get_conceptnet_relations_filtered_to_text():
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

def create_input_list(head_events, relations):
    input_list = []
    for relation in relations:
        for head_event in head_events:
            input_list.append(head_event + '\t' + relation)
    return input_list

def create_input_file(head_events, relations):
    num_lines = 0
    with open(DATA_PATH + KG + '_comet_input_file.tsv', 'w+') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter="\t")
        for relation in relations:
            for head_event in head_events:
                num_lines += 1
                # some keywords contain underscore, for eg: "chess_player" --> "chess player"
                tsv_writer.writerow([head_event.lower().replace('_', ' '), relation])
    print("Number of lines written to input_file:", num_lines)


if __name__ == '__main__':

    # get keywords (same for all KGs)
    keywords = get_keywords()
    # country_keywords = get_country_keywords()
    # relig_keywords = get_relig_keywords()
    # gender_keywords = get_gender_keywords()
    # profession_keywords = get_profession_keywords()

    # print("length all keywords:", len(keywords))
    # print("length country keywords:", len(country_keywords))
    # print("length religion keywords:", len(relig_keywords))
    # print("length gender keywords:", len(gender_keywords))
    # print("length profession keywords:", len(profession_keywords))
    # print()

    # # load train, dev, and test data (if necessary)
    # train = get_data('train.tsv')
    # dev = get_data('dev.tsv')
    # test = get_data('test.tsv')
    # all_data = pd.concat([train, dev, test], axis=0, ignore_index=True)
    # print("length train:", len(train))
    # print("length dev:", len(dev))
    # print("length test:", len(test))
    # print("length all data:", len(all_data))
    # print()

    relations_unfiltered = get_conceptnet_relations()
    relations_filtered = get_conceptnet_relations_filtered()
    to_remove = list(set(relations_unfiltered) - set(relations_filtered))
    print("Unfiltered - filtered ConceptNet relations:", to_remove)
    print("Sum of what we remove and what we keep (exp: 47):", len(to_remove) + len(relations_filtered))
    print()

    if KG == 'atomic': 
        relations = get_atomic_relations()
    elif KG == 'conceptnet':
        relations = get_conceptnet_relations_filtered()
    
    print("Relations:")
    print(relations)
    print("Number of relations:", len(relations))
    print()

    # # test input_list (see what file would look like without creating it)
    # input_list = create_input_list(get_keywords(), relations)
    # print(input_list)
    # print()
    # print("length of input_list:", len(input_list))

    # # create comet input file
    # create_input_file(get_keywords(), relations)