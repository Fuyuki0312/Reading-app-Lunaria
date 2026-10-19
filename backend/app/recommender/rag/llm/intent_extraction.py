# Problems:
# - This module needs evaluation.

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
) -> dict[str, list]:


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
        print("ValueError in intent_extraction.py: Invalid entity indices in LLM response.")
        return {'entities': [], 'excluded_genres': []}

    intents = {item.index: item.intent for item in response.results}

    return {
        "entities": [
            {**entity, "intent": intents[i]}
            for i, entity in enumerate(entities)
        ],
        "excluded_genres": [
            genre
            for genre in response.excluded_genres
            if genre in book_services.get_all_genres()
        ]
    }

# return example:

"""
{'entities': [{'end': 44,
               'intent': 'reference',
               'name': 'The Cartographer of Moonfall',
               'start': 16,
               'type': 'book'},
              {'end': 79,
               'intent': 'exclude',
               'name': 'Jeshine',
               'start': 72,
               'type': 'author'},
              {'end': 121,
               'intent': 'prefer',
               'name': 'Avery Lorne',
               'start': 110,
               'type': 'author'}],
 'excluded_genres': ['Comedy']}
"""