from app.config import Config
from app.model.llm_response import RecommendationOutputForm

from pathlib import Path
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

config = Config()


env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path) # Get OpenAI API


model = init_chat_model(config.LLM).with_structured_output(
    RecommendationOutputForm,
    method="json_schema",
    strict=True
)


def get_llm():

    return model
