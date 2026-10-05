from app.config import Config

from app.recommender.rag.llm.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate


config = Config()

def recommend_books(
        user_genre_preference: list[str],
        user_preference_description: str,
        books: list[dict]
) -> list[dict]:

    if not user_genre_preference:  # if user_genre_preference == []:
        user_genre_preference = ["Any"]

    model = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            config.get_system_prompt_for_model(books)
        ),
        (
            "human",
            "My genre preferences: {user_genre_preference}\n" +
            "Other descriptions of preferences: {user_preference_description}"
        )
    ])

    chain = prompt | model

    llm_response = chain.invoke({
        "user_genre_preference": user_genre_preference,
        "user_preference_description": user_preference_description
    })

    recommendations = llm_response.recommendation

    return recommendations  # List

