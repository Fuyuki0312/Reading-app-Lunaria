from pprint import pprint

from app.recommender.rag.retrieval.entity_matching import match_entities
from app.recommender.rag.llm.intent_extraction import extract_intents

text = (
    "I was into The Cartographer of Moonfall, "
    "but I do not want to read Jeshine's books anymore. "
    "Now I prefer Avery Lorne."
    "I dislike Comedy."
)

entities = match_entities(text)

results = extract_intents(text, entities)

pprint(results)