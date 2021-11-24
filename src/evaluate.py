import json
import pickle

import pandas as pd
import sklearn.metrics as metrics
import typer
from loguru import logger

app = typer.Typer()

@app.command()
def evaluate(
    preds_path: str = typer.Option(..., help="Path to predicted labels (csv.)"),
    true_path: str = typer.Option(..., help="Path to true labels (csv)."),
    label_encoder_path: str = typer.Option(..., help="Path label encoder (pickle)."),
    metrics_path: str = typer.Option(..., help="Path to save metrics json."),
):

    # Load label_encoder object

    with open(label_encoder_path, "rb") as fd:
        label_encoder = pickle.load(fd)
    logger.info("Loaded label encoder from {}", label_encoder_path)

    # NOTE: This scripts expects csv files with two columns [Category, Message]

    true = pd.read_csv(true_path)
    y_true = true["Category"].values

    preds = pd.read_csv(preds_path)
    preds = label_encoder.inverse_transform(preds).ravel()

    results = metrics.classification_report(y_true, preds, output_dict=True)

    with open(metrics_path, "w") as fd:
        json.dump(results, fd, indent=4)
    logger.info("Saved metrics to {}", metrics_path)


if __name__ == "__main__":
    app()
