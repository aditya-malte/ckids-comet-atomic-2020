import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from collections import defaultdict
import matplotlib
import argparse
import operator

regard_output_file_path = '/nas/home/malte/ckids-comet-atomic-2020/nlg-bias/models/bert_regard_v2_large/conceptnet_bias_input_predictions.txt'
country_metrics_dict = dict()
religion_metrics_dict = dict()
gender_metrics_dict = dict()
profession_metrics_dict = dict()
neutral_metrics_dict = dict()

def get_country_keywords():
	return ['african_american','Armenian','Persian','American','Filipino','English','Norwegian','Dutch','Israeli','Nigerian', 'Ethiopia', 'Europe', 'European', 'Russian', 'Ukraine',
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
    'Cape_Verde', 'Portugal', 'Austria', 'Singaporean', 'Netherlands']

def get_relig_keywords():
	return ['Sharia', 'Jihad', 'Christian', 'Muslim', 'Islam', 'Hindu',
    'Mohammed', 'church',  'Quran','Bible','Brahmin','Holy_Trinity']

def get_gender_keywords():
	return ['she','he','hers','him','her','herself', 'himself', 'his','woman','man','female','male','lady','gentleman','ladies','gentlemen','girl','boy' ,'sir', 'ma_am','mother','father','stepmother','stepfather','daughter', 'son','sister', 'brother',  'grandmother',   'grandfather' ,
    'mommy', 'daddy','wife','husband','bride', 'groom','girlfriend', 'boyfriend','schoolgirl' , 'schoolboy']

def get_profession_keywords():
	return ['barber', 'coach', 'businessperson', 'football_player', 'construction_worker', 'manager',
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

# match the keywords to what they are in the bias output
def process_keywords(keywords):
    for i in range(len(keywords)):
        keyword = keywords[i]
        keywords[i] = keyword.lower().replace('_', ' ')
    return keywords

# add score to metrics dictionary
def add_score(keyword, score, metrics_dict):
    if score == -1:
        metrics_dict[keyword]['negative_count'] += 1
        metrics_dict[keyword]['total_count'] += 1
    elif score == 0:
        metrics_dict[keyword]['neutral_count'] += 1
        metrics_dict[keyword]['total_count'] += 1
    elif score == 1:
        metrics_dict[keyword]['positive_count'] += 1
        metrics_dict[keyword]['total_count'] += 1
    else:
        print("ERROR: invalid score:", score)

# Adapted from Nina's code
def get_stats(metrics_dict):
    negative_box_plot =[]
    neutral_box_plot =[]
    positive_box_plot =[]

    for keyword in metrics_dict:
        negative_count = metrics_dict[keyword]['negative_count']
        positive_count = metrics_dict[keyword]['positive_count']
        neutral_count = metrics_dict[keyword]['neutral_count']
        total = metrics_dict[keyword]['total_count']

        if (total != 0):
            negative_box_plot.append((negative_count/total)*100)
            positive_box_plot.append((positive_count/total)*100)
            neutral_box_plot.append((neutral_count/total)*100)
        else:
            negative_box_plot.append(0.0)
            positive_box_plot.append(0.0)
            neutral_box_plot.append(0.0)
    
    return negative_box_plot, neutral_box_plot, positive_box_plot

# Adapted from Nina's code
def plotting(country_negative_box_plot,gender_negative_box_plot,relig_negative_box_plot,prof_negative_box_plot,country_positive_box_plot,gender_positive_box_plot,relig_positive_box_plot,prof_positive_box_plot):
    # plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plt.subplots(figsize=(10, 8))

    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)
        plt.setp(bp['fliers'], color=color)

    neg_data = [country_negative_box_plot,gender_negative_box_plot,relig_negative_box_plot,prof_negative_box_plot]
    pos_data = [country_positive_box_plot,gender_positive_box_plot,relig_positive_box_plot,prof_positive_box_plot]

    flierprops1 = dict(markeredgecolor= '#D7191C')
    flierprops2 = dict(markeredgecolor='#2C7BB6')
    bpl = plt.boxplot(neg_data,showfliers=True ,showmeans=True, positions=np.array(range(len(neg_data)))*2.0-0.4,  widths=0.6,flierprops=flierprops1)
    bpr = plt.boxplot(pos_data,showfliers=True ,showmeans=True, positions=np.array(range(len(pos_data)))*2.0+0.4, widths=0.6,flierprops=flierprops2)
    set_box_color(bpl, '#D7191C') 
    set_box_color(bpr, '#2C7BB6')

    plt.plot([], c='#D7191C', label='Negative')
    plt.plot([], c='#2C7BB6', label='Positive')
    plt.legend(prop={'size': 20})

    ticks =["Origin","Gender","Religion","Profession"]
    plt.xticks(range(0, len(ticks) * 2, 2), ticks)
    plt.xlim(-2, len(ticks)*2)

    ax.set_ylabel('Regard (%)',fontsize=35)
    ax.set_title("ConceptNet Regard",fontsize=40)
    plt.yticks(fontsize=27)
    plt.xticks(fontsize=30)
    plt.xlim([-1,7])
    fig.tight_layout()

    plt.show()
    plt.savefig('plot.png')


if __name__ == "__main__":

    country_keywords = process_keywords(get_country_keywords())
    religion_keywords = process_keywords(get_relig_keywords())
    gender_keywords = process_keywords(get_gender_keywords())
    profession_keywords = process_keywords(get_profession_keywords())
    neutral_keywords = ['this person']

    with open(regard_output_file_path, 'r') as file:
        lines_list = file.readlines()
        for line in lines_list:
            split_line = line.split('\t')
            score = int(split_line[0])
            keyword = split_line[1]

            if keyword in country_keywords:
                if keyword not in country_metrics_dict:
                    country_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'total_count': 0}
                add_score(keyword, score, country_metrics_dict)
            
            elif keyword in religion_keywords:
                if keyword not in religion_metrics_dict:
                    religion_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'total_count': 0}
                add_score(keyword, score, religion_metrics_dict)
            
            elif keyword in gender_keywords:
                if keyword not in gender_metrics_dict:
                    gender_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'total_count': 0}
                add_score(keyword, score, gender_metrics_dict)
            
            elif keyword in profession_keywords:
                if keyword not in profession_metrics_dict:
                    profession_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'total_count': 0}
                add_score(keyword, score, profession_metrics_dict)
            
            elif keyword in neutral_keywords:
                if keyword not in neutral_metrics_dict:
                    neutral_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'total_count': 0}
                add_score(keyword, score, neutral_metrics_dict)
            else:
                print("ERROR: could not find keyword:", keyword)
    
    country_negative_box_plot, country_neutral_box_plot, country_positive_box_plot= get_stats(country_metrics_dict)
    gender_negative_box_plot, gender_neutral_box_plot, gender_positive_box_plot = get_stats(gender_metrics_dict)
    relig_negative_box_plot, relig_neutral_box_plot, relig_positive_box_plot = get_stats(religion_metrics_dict)
    prof_negative_box_plot, prof_neutral_box_plot, prof_positive_box_plot = get_stats(profession_metrics_dict)

    plotting(country_negative_box_plot,gender_negative_box_plot,relig_negative_box_plot,prof_negative_box_plot,
            country_positive_box_plot,gender_positive_box_plot,relig_positive_box_plot,prof_positive_box_plot)