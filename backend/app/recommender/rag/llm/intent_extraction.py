# At the time being, I am using GPT-5 nano to extract user's intents.
# Maybe, it would be better to use a cheaper LLM.

import json
from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import Config
from app.model.model_for_intent_extraction import IntentOutput


load_dotenv(
    Path(__file__).resolve().parent.parent.parent.parent / ".env"
)

model = init_chat_model(Config().LLM).with_structured_output(
    IntentOutput,
    method="json_schema",
    strict=True
)

def extract_intents(
    user_description: str,
    entities: list[dict]
) -> list[dict]:

    if not entities:
        return []

    response = model.invoke([ # Throw this to config
        SystemMessage(content="""
        Identify the user's CURRENT intent toward each detected entity.

        Labels:
        - prefer: currently liked or preferred
        - exclude: explicitly unwanted or rejected
        - reference: a book used as an example for finding similar books
        - neutral: merely mentioned, unclear, or insufficient evidence

        Consider negation, past preferences, and changes in preference.
        Do not infer an exclusion without clear evidence.
        Return exactly one result for each entity, using its index.
        """),

        HumanMessage(content=json.dumps({
            "user_description": user_description,
            "entities": [
                {
                    "index": i,
                    "type": entity["type"],
                    "name": entity["name"]
                }
                for i, entity in enumerate(entities)
            ]
        }, ensure_ascii=False))
    ])

    indices = [item.index for item in response.results]

    if sorted(indices) != list(range(len(entities))):
        raise ValueError("Invalid entity indices in LLM response.")

    intents = {item.index: item.intent for item in response.results}

    return [
        {**entity, "intent": intents[i]}
        for i, entity in enumerate(entities)
    ]