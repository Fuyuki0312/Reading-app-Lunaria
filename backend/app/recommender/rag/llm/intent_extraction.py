# Problems:
# - This module needs evaluation.
# - This module does not process disliked genres.

import json
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

from app.config import Config
from app.model.model_for_intent_extraction import IntentOutput
from app.services.book_services import get_book_services


book_services = get_book_services()

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


    response = model.invoke([
        SystemMessage(content=Config().get_prompt_for_llm_in_intent_extraction()),

        HumanMessage(content=json.dumps({
            "user_description": user_description,
            "entities": [
                {
                    "index": i,
                    "type": entity["type"],
                    "name": entity["name"]
                }
                for i, entity in enumerate(entities)
            ],
            "known_genres": list(book_services.get_all_genres())
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