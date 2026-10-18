from pprint import pprint
import torch

from app.recommender.rag.retrieval.entity_matching import match_entities
from app.recommender.rag.llm.intent_extraction import extract_intents

torch.manual_seed(42)

text = (
    "I enjoy reading The Cartographer of Moonfall, "
    "but I do not want to read Jeshine's books anymore. "
    "Now I prefer Avery Lorne. "
    "I dislike Comedy."
)

entities = match_entities(text)

results = extract_intents(text, entities)

pprint(results)


"""
output example:

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