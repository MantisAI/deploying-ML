from fastapi import FastAPI
from pydantic import BaseModel

from src.utils import load_object


clf = load_object("model.pk", rev="feature/api")
label_encoder = load_object("label_encoder.pk", rev="feature/api")
vectorizer = load_object("vectorizer.pk", rev="feature/api")


class TextMessage(BaseModel):
    text: str = "Text message goes here..."


app = FastAPI()


async def predict_(text: str):
    """Return an ML Code predicted by the model asynchronously"""
    pred = vectorizer.transform([text])
    pred = clf.predict(pred)
    pred = label_encoder.inverse_transform(pred)

    return pred[0]


@app.post("/predict")
async def predict(text_message: TextMessage):
    out = {}
    out["result"] = await predict_(text_message.text)

    return out
