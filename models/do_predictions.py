from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer
import pandas as pd
import csv

model_path = "/nas/home/malte/ckids-comet-atomic-2020/models/comet_atomic2020_gpt2/model_files/checkpoint_0"
input_file_path = "/nas/home/malte/ckids-comet-atomic-2020/data/test-file.tsv"
output_file_path = "/nas/home/malte/ckids-comet-atomic-2020/data/conceptnet_comet_output_file.tsv"

# get model and tokenizer set up
model = AutoModelWithLMHead.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
text2text_generator = pipeline("text2text-generation",model=model, tokenizer=tokenizer)

# open input file
input_file = pd.read_csv(input_file_path, names = ['head_event', 'relation', 'tail_event'], encoding='latin-1', sep="\t")

# make predictions and write to output file
with open(output_file_path, 'w+') as output_file:
    tsv_writer = csv.writer(output_file, delimiter="\t")
    for index, row in input_file.iterrows():
        input_str = row['head_event'] + ' ' + row['relation']
        pred = text2text_generator(input_str)[0]['generated_text'].replace('<pad>', '')
        tsv_writer.writerow([row['head_event'], row['relation'], pred])
