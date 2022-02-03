import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import matplotlib.pyplot as plt
import numpy as np
from analyze_regard_unmasked import get_country_keywords
from analyze_regard_unmasked import get_relig_keywords
from analyze_regard_unmasked import get_gender_keywords
from analyze_regard_unmasked import get_profession_keywords
from analyze_regard_unmasked import process_keywords
from analyze_regard_unmasked import get_stats
from analyze_regard_unmasked import get_negative_outliers, get_positive_outlier, print_outlier

# TODO: modify parameters depending on use case
BIAS_INPUT_FILE_PATH = "/nas/home/malte/ckids-comet-atomic-2020/nlg-bias/data/conceptnet_t5base_bias_input.txt"
SENTIMENT_OUTPUT_FILE_PATH = "/nas/home/malte/ckids-comet-atomic-2020/data/conceptnet_t5base_sentiment_output.tsv"
image_name = 'conceptnet_t5base_sentiment.png'
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
    neutral_keywords = ['this person']

    # plot results of sentiment analyzer
    with open(SENTIMENT_OUTPUT_FILE_PATH, 'r') as file:
        lines_list = file.readlines()
        for line in lines_list:
            split_line = line.split('\t')
            score = float(split_line[0])
            keyword = split_line[1]
            relation = split_line[2]

            if keyword in country_keywords:
                if keyword not in country_metrics_dict:
                    country_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'other_count': 0, 'total_count': 0}
                add_score(keyword, score, country_metrics_dict)
            
            elif keyword in religion_keywords:
                if keyword not in religion_metrics_dict:
                    religion_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'other_count': 0, 'total_count': 0}
                add_score(keyword, score, religion_metrics_dict)
            
            elif keyword in gender_keywords:
                if keyword not in gender_metrics_dict:
                    gender_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'other_count': 0, 'total_count': 0}
                add_score(keyword, score, gender_metrics_dict)
            
            elif keyword in profession_keywords:
                if keyword not in profession_metrics_dict:
                    profession_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'other_count': 0, 'total_count': 0}
                add_score(keyword, score, profession_metrics_dict)
            
            elif keyword in neutral_keywords:
                if keyword not in neutral_metrics_dict:
                    neutral_metrics_dict[keyword] = {'negative_count': 0, 'neutral_count': 0, 'positive_count': 0, 'other_count': 0, 'total_count': 0}
                add_score(keyword, score, neutral_metrics_dict)
            else:
                print("ERROR: could not find keyword:", keyword)

    # get data for creating box plots
    country_negative_box_plot, country_neutral_box_plot, country_positive_box_plot = get_stats(country_metrics_dict)
    gender_negative_box_plot, gender_neutral_box_plot, gender_positive_box_plot = get_stats(gender_metrics_dict)
    relig_negative_box_plot, relig_neutral_box_plot, relig_positive_box_plot = get_stats(religion_metrics_dict)
    prof_negative_box_plot, prof_neutral_box_plot, prof_positive_box_plot = get_stats(profession_metrics_dict)

    # create the box plot
    plotting(country_negative_box_plot,gender_negative_box_plot,relig_negative_box_plot,prof_negative_box_plot,
            country_positive_box_plot,gender_positive_box_plot,relig_positive_box_plot,prof_positive_box_plot)

    # find outliers
    print("---ORIGIN (negative)\n")
    get_negative_outliers(0.14, country_keywords, country_metrics_dict)
    print("---ORIGIN (positive)\n")
    get_positive_outlier(0.04, country_keywords, country_metrics_dict)
    print("---GENDER (negative)\n")
    get_negative_outliers(0.15, gender_keywords, gender_metrics_dict)
    print("---GENDER (positive)\n")
    get_positive_outlier(0.10, gender_keywords, gender_metrics_dict)
    print("---RELIGION (negative)\n")
    get_negative_outliers(0.20, religion_keywords, religion_metrics_dict)
    print("---RELIGION (positive)\n")
    get_positive_outlier(0.10, religion_keywords, religion_metrics_dict)
    print("---PROFESSION (negative)\n")
    get_negative_outliers(0.10, profession_keywords, profession_metrics_dict)
    print("---PROFESSION (positive)\n")
    get_positive_outlier(0.15, profession_keywords, profession_metrics_dict)

    print()
    print("Baselines:")
    print("Number of times 'this person' was given negative score: {0} ({1}%)".format(neutral_metrics_dict['this person']['negative_count'], round(neutral_metrics_dict['this person']['negative_count'] / neutral_metrics_dict['this person']['total_count'] * 100, 3)))
    print("Number of times 'this person' was given positive score: {0} ({1}%)".format(neutral_metrics_dict['this person']['positive_count'], round(neutral_metrics_dict['this person']['positive_count'] / neutral_metrics_dict['this person']['total_count'] * 100, 3)))
    print("Number of times 'this person' was given neutral score: {0} ({1}%)".format(neutral_metrics_dict['this person']['neutral_count'], round(neutral_metrics_dict['this person']['neutral_count'] / neutral_metrics_dict['this person']['total_count'] * 100, 3)))
    print("Number of times 'this person' was given other score: {0} ({1}%)".format(neutral_metrics_dict['this person']['other_count'], round(neutral_metrics_dict['this person']['other_count'] / neutral_metrics_dict['this person']['total_count'] * 100, 3)))
    print("Total number of occurrences for 'this person':", neutral_metrics_dict['this person']['total_count'])