import os

from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel

from src.utils import load_object

# Check for env vars which set the DVC remote and the git revision

REV = os.getenv("REV", "main")
REMOTE = os.getenv("REMOTE", "s3")

# Load model artefacts from cache/dvc

clf = load_object("model.pk", rev=REV, remote=REMOTE)
label_encoder = load_object("label_encoder.pk", rev=REV, remote=REMOTE)
vectorizer = load_object("vectorizer.pk", rev=REV, remote=REMOTE)

# Define a pydantic class for handling the incoming data


class TextMessage(BaseModel):
    text: str = "Text message goes here..."


app = FastAPI()


async def predict_(text: str):
    """Return classification the model asynchronously"""
    logger.info("Recieved text {}", text)
    pred = vectorizer.transform([text])
    pred = clf.predict(pred)
    pred = label_encoder.inverse_transform(pred)
    logger.info("Returning class {}", pred[0])

    return pred[0]


@app.post("/predict")
async def predict(text_message: TextMessage):
    """The /predict endpoint"""
    out = dict()
    out["result"] = await predict_(text_message.text)

    return out
