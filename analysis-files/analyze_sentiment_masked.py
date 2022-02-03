import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter as counter
from analyze_regard_masked import get_country_keywords
from analyze_regard_masked import get_relig_keywords
from analyze_regard_masked import get_gender_keywords
from analyze_regard_masked import get_profession_keywords
from analyze_regard_masked import process_keywords
from analyze_regard_masked import get_stats

# TODO: modify parameters depending on use case
BIAS_INPUT_FILE_PATH = "/nas/home/malte/ckids-comet-atomic-2020/nlg-bias/data/conceptnet_t5base_bias_input.txt"
SENTIMENT_OUTPUT_FILE_PATH = "/nas/home/malte/ckids-comet-atomic-2020/data/conceptnet_t5base_sentiment_output.tsv"
image_name = 'conceptnet_t5base_sentiment_masked.png'
image_title = 'Comet Sentiment (trained on T5-base and ConceptNet)'

country_metrics_dict = dict()
religion_metrics_dict = dict()
gender_metrics_dict = dict()
profession_metrics_dict = dict()
neutral_metrics_dict = dict()

# get bias input file for doing analysis
def get_input_file(file_name):
    return pd.read_csv(file_name, names = ['head_event', 'relation', 'tail_event'], encoding='latin-1', sep="\t")

# run Vader sentiment analyzer on masked and unmasked sentences
def run_sentiment_analyzer(sentences_df):
    sia = SentimentIntensityAnalyzer()
    with open(SENTIMENT_OUTPUT_FILE_PATH, 'w+') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter="\t")
        for index, row in sentences_df.iterrows():
            if pd.isnull(row['tail_event']):
                tail = ''
            else:
                tail = row['tail_event']
            input_str = row['head_event'] + ' ' + row['relation'] + ' ' + tail
            sentiment_dict = sia.polarity_scores(input_str)
            tsv_writer.writerow([sentiment_dict['compound'], row['head_event'], row['relation'], row['tail_event']])

# # add score to metrics dictionary
# def add_score(score, metrics_dict):
#     if score >= 0.05: 
#         if 'positive_count' in metrics_dict:
#             metrics_dict['positive_count'] += 1
#         else:
#             metrics_dict['positive_count'] = 0
#     elif score <= -0.05:
#         if 'negative_count' in metrics_dict:
#             metrics_dict['negative_count'] += 1
#         else:
#             metrics_dict['negative_count'] = 0
#     else:
#         if 'neutral_count' in metrics_dict:
#             metrics_dict['neutral_count'] += 1
#         else:
#             metrics_dict['neutral_count'] = 0
    
#     if 'total_count' in metrics_dict:
#         metrics_dict['total_count'] += 1
#     else:
#         metrics_dict['total_count'] = 0

# add score to metrics dictionary
def add_score(keyword, score, metrics_dict):
    if score >= 0.05: 
        metrics_dict[keyword]['positive_count'] += 1
        metrics_dict[keyword]['total_count'] += 1
    elif score <= -0.05:
        metrics_dict[keyword]['negative_count'] += 1
        metrics_dict[keyword]['total_count'] += 1
    else:
        metrics_dict[keyword]['neutral_count'] += 1
        metrics_dict[keyword]['total_count'] += 1

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

    ax.set_ylabel('Sentiment (%)', fontsize=35)
    ax.set_title(image_title, fontsize=20)
    plt.yticks(fontsize=27)
    plt.xticks(fontsize=30)
    plt.xlim([-1,7])
    fig.tight_layout()

    plt.savefig(image_name)

if __name__ == "__main__":

    # # run sentiment classifier and store results in file
    # sentences_df = get_input_file(BIAS_INPUT_FILE_PATH)
    # run_sentiment_analyzer(sentences_df)

    country_keywords = process_keywords(get_country_keywords())
    religion_keywords = process_keywords(get_relig_keywords())
    gender_keywords = process_keywords(get_gender_keywords())
    profession_keywords = process_keywords(get_profession_keywords())

    # count number of times the regard score for masked sentence is different from unmasked sentence
    count = 0
    keyword_list = []

    # plot results of sentiment analyzer
    with open(SENTIMENT_OUTPUT_FILE_PATH, 'r') as file:
        lines_list = file.readlines()

        for i in range(0, len(lines_list)-1, 2):
            line_unmasked = lines_list[i].split('\t')
            line_masked = lines_list[i+1].split('\t')

            # find score and keyword
            keyword = line_unmasked[1]
            score_masked = float(line_masked[0])
            score_unmasked = float(line_unmasked[0])

            if score_masked != score_unmasked:
                count += 1
                keyword_list.append(keyword)
            
            if keyword in country_keywords:
                if keyword not in country_metrics_dict:
                    country_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'other_count': 0, 'total_count': 0}
                add_score(keyword, score_masked, country_metrics_dict)
            
            elif keyword in religion_keywords:
                if keyword not in religion_metrics_dict:
                    religion_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'other_count': 0, 'total_count': 0}
                add_score(keyword, score_masked, religion_metrics_dict)
            
            elif keyword in gender_keywords:
                if keyword not in gender_metrics_dict:
                    gender_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'other_count': 0, 'total_count': 0}
                add_score(keyword, score_masked, gender_metrics_dict)
            
            elif keyword in profession_keywords:
                if keyword not in profession_metrics_dict:
                    profession_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'other_count': 0, 'total_count': 0}
                add_score(keyword, score_masked, profession_metrics_dict)
            
            elif keyword in neutral_keywords:
                if keyword not in neutral_metrics_dict:
                    neutral_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'other_count': 0, 'total_count': 0}
                add_score(keyword, score_masked, neutral_metrics_dict)
            else:
                print("ERROR: could not find keyword:", keyword)

            # # update scores in appropriate dictionary
            # if keyword in country_keywords:
            #     add_score(score_masked, country_metrics_dict)
            # elif keyword in gender_keywords:
            #     add_score(score_masked, gender_metrics_dict)
            # elif keyword in religion_keywords:
            #     add_score(score_masked, religion_metrics_dict)
            # elif keyword in profession_keywords:
            #     add_score(score_masked, profession_metrics_dict)

    # get data for creating box plots
    country_negative_box_plot, country_neutral_box_plot, country_positive_box_plot = get_stats(country_metrics_dict)
    gender_negative_box_plot, gender_neutral_box_plot, gender_positive_box_plot = get_stats(gender_metrics_dict)
    relig_negative_box_plot, relig_neutral_box_plot, relig_positive_box_plot = get_stats(religion_metrics_dict)
    prof_negative_box_plot, prof_neutral_box_plot, prof_positive_box_plot = get_stats(profession_metrics_dict)

    # create the box plot
    plotting(country_negative_box_plot,gender_negative_box_plot,relig_negative_box_plot,prof_negative_box_plot,
            country_positive_box_plot,gender_positive_box_plot,relig_positive_box_plot,prof_positive_box_plot)

    print("Number of times masked sentiment score does not equal unmasked score:", count)
    print("List of keywords:")
    print(counter(keyword_list))