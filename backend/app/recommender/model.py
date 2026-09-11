from transformers import AutoProcessor, AutoModelForMultimodalLM
from app.config import Config

config = Config()

MODEL_NAME = config.MODEL_NAME

processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForMultimodalLM.from_pretrained(MODEL_NAME, device_map="auto")


def get_model_and_processor():

    return model, processor
