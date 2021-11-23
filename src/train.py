"""
Train a model using tf-idf and svm and save predictions to disk
"""
import pickle

import pandas as pd
import yaml
from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

# Load parameters from params file

with open("params.yaml", "r") as fd:
    params = yaml.safe_load(fd)
params = params["train"]
kernel = params["kernel"]
poly_degree = params["poly_degree"]
reg_param = params["reg_param"]


# Set paths for loading and saving

train_path = "./data/processed/train.csv"
test_path = "./data/processed/test.csv"
train_pred_path = "./results/train_preds.csv"
test_pred_path = "./results/test_preds.csv"
label_encoder_path = "./models/label_encoder.pk"

# Read train and test data

train = pd.read_csv(train_path)
logger.info("Loaded {} rows from {}", len(train), train_path)

test = pd.read_csv(test_path)
logger.info("Loaded {} rows from {}", len(test), test_path)

# Tfidf vectorize the data

vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform(train["Message"])
X_test = vectorizer.transform(test["Message"])

# Encode the labels

label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(train["Category"])
y_test = label_encoder.transform(test["Category"])

# Fit a classifier

clf = SVC(C=reg_param, kernel=kernel, degree=poly_degree)
clf.fit(X_train, y_train)

# Make predictions on train and test, and save to disk

train_preds = clf.predict(X_train)
pd.DataFrame(train_preds).to_csv(train_pred_path)
logger.info("Saved {} predictions to {}", len(train_preds), train_pred_path)

test_preds = clf.predict(X_test)
pd.DataFrame(test_preds).to_csv(test_pred_path)
logger.info("Saved {} predictions to {}", len(test_preds), test_pred_path)

# Save objects that we need to re-use later

with open(label_encoder_path, "wb") as fd:
    pickle.dump(label_encoder, fd)
logger.info("Saved label_encoder to {}", label_encoder_path)
