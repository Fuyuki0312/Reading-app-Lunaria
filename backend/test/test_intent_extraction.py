from pprint import pprint

from app.recommender.rag.retrieval.entity_matching import match_entities
from app.recommender.rag.llm.intent_extraction import extract_intents

text = (
    "I loved The Silence Between Stars, "
    "but I don't want Iris Vale anymore. "
    "Now I prefer Nora Vale."
)

entities = match_entities(text)

results = extract_intents(text, entities)

pprint(results)