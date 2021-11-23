import json
import pickle

import pandas as pd
import sklearn.metrics as metrics

preds_path = "./results/test_preds.csv"
true_path = "./data/processed/test.csv"
label_encoder_path = "./models/label_encoder.pk"
metrics_path = "./results/metrics.json"

with open(label_encoder_path, "rb") as fd:
    label_encoder = pickle.load(fd)

true = pd.read_csv(true_path)
y_true = true["Category"].values

preds = pd.read_csv(preds_path)
preds = label_encoder.inverse_transform(preds).ravel()

results = metrics.classification_report(y_true, preds, output_dict=True)

with open(metrics_path, "w") as fd:
    json.dump(results, fd, indent=4)
