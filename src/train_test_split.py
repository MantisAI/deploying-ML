"""
Create a train test split and save to disk
"""
import random

import pandas as pd
import yaml
from loguru import logger

with open("params.yaml", "r") as fd:
    params = yaml.safe_load(fd)
params = params["train_test_split"]

random_state = params["random_state"]
test_prop = params["test_prop"]

data_path = "data/processed/spam_data.csv"
train_path = "data/processed/train.csv"
test_path = "data/processed/test.csv"

data = pd.read_csv(data_path)

idx = list(range(0, len(data)))
random.seed(params["random_state"])
random.shuffle(idx)

train_size = round(len(data) * (1 - test_prop))
logger.info("Splitting data with train: {} and test: {}", (1 - test_prop), test_prop)

train_set = data[0:train_size]
test_set = data[train_size:]

train_set.to_csv(train_path, index=False)
logger.info("Saved {} rows training set to {}", len(train_set), train_path)

test_set.to_csv(test_path, index=False)
logger.info("Saved {} rows testing set to {}", len(test_set), test_path)
