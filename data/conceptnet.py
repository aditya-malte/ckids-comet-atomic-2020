import pandas as pd
import numpy as np
from os.path import join

FILE_PATH = "/data/malte/kgtk_conceptnet.tsv"
DATA_DIR = "/nas/home/malte/ckids-comet-atomic-2020/data"

data = (pd.read_csv(FILE_PATH, sep="\t")[["node1;label", "relation;label", "node2;label"]]).dropna()
train, dev, test = np.split(data.sample(frac=1, random_state=42).sample(frac=1, random_state=42), 
                       [int(0.8*len(data)), int(0.9*len(data))])

train.to_csv(join(DATA_DIR, 'train.tsv'), index=None, sep="\t", header=None)
dev.to_csv(join(DATA_DIR,'dev.tsv'), index=None, sep="\t", header=None)
test.to_csv(join(DATA_DIR,'test.tsv'), index=None, sep="\t", header=None)
