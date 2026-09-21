from app.recommender.rag.llm.client import get_client
from app.config import Config

import json

config = Config()

def recommend_books(
        user_genre_preference: list[str],
        user_preference_description: str,
        books: list[dict]
) -> list[dict]:

    client = get_client()

    if not user_genre_preference: # if user_genre_preference == []:
        user_genre_preference = ["Any"]


    llm_response = client.responses.create(
        model=config.LLM,
        instructions=config.get_system_prompt_for_model(books=books),
        input=f"My genre preferences: {user_genre_preference}\nOther descriptions of preferences: {user_preference_description}"
    )

    json_outputs = json.loads(llm_response.output_text)

    recommendations = json_outputs["recommendations"]

    return recommendations # List

