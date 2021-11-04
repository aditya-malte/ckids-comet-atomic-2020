import pandas as pd
import random
import argparse
import numpy as np
from sklearn.model_selection import train_test_split



data = pd.read_csv('wikidata-cs-20200504.tsv', sep='\t', header=0)
wikidata = data.loc[:,['node1;label','relation','node2;label']]

X = wikidata.loc[:,['node1;label','relation']]
y = wikidata.loc[:,['node2;label']]

test_size = 0.1
dev_size = 0.1

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size = test_size + dev_size)
X_test, X_dev, y_test, y_dev = train_test_split(X_temp, y_temp, test_size = dev_size / (test_size + dev_size))

wiki_train = pd.concat([X_train,y_train],axis=1)
wiki_test = pd.concat([X_test,y_test],axis=1)
wiki_dev = pd.concat([X_dev,y_dev],axis=1)

wiki_train.to_csv("./data/wiki_train.tsv", index=False, sep='\t', header=None)
wiki_test.to_csv("./data/wiki_test.tsv", index=False, sep='\t', header=None)
wiki_dev.to_csv("./data/wiki_dev.tsv", index=False, sep='\t', header=None)
