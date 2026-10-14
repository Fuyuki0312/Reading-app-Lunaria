# Problems:
# - GPT-5 nano is an overkill.
# - This module needs evaluation.
# - This module does not process disliked genres.

import json
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

from app.config import Config
from app.model.model_for_intent_extraction import IntentOutput


model = ChatOllama(
    model=Config().LLM_FOR_INTENT_EXTRACTION,
    reasoning=False
).with_structured_output(
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

# return example:

"""
[{'end': 33,
  'intent': 'neutral',
  'name': 'The Silence Between Stars',
  'start': 8,
  'type': 'book'},
 {'end': 61,
  'intent': 'exclude',
  'name': 'Iris Vale',
  'start': 52,
  'type': 'author'}]
"""