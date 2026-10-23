from app.model.llm_response import RecommendationForm
from app.recommender.rag.llm.llm_recommendation import recommend_books_with_llm
from app.recommender.rag.llm.intent_extraction import extract_intents
from app.recommender.rag.retrieval import retrieve_books
from app.recommender.rag.retrieval import match_entities
from app.services.book_services import get_book_services


book_services = get_book_services()

def recommend_books_with_rag(
        user_genre_preference: list[str],
        user_preference_description: str
) -> list[RecommendationForm]:
    """
    This function run in the below order:

    1. extract entities and extract intents (see more about "entities" in entity_matching.py)
    2. retrieve books
    2.5. index books with ids
    3. llm recommends books
    """


    intents = extract_intents(
        user_description=user_preference_description,
        entities=match_entities(user_preference_description)
    )


    excluded_genres = None
    excluded_authors = []

    if intents:

        for entity in intents["entities"]:

            if entity["intent"] == "exclude":

                if entity["type"] == "author":
                    excluded_authors.append(entity["name"])
                elif entity["type"] == "book":
                    print("WARNING: Detected disliked books in user description. "
                          "RAG does not exclude disliked books for the time being.")
                else:
                    print("WARNING: Detected unknown type of which intent is 'excluded'.")

        if intents["excluded_genres"]:
            excluded_genres = intents["excluded_genres"]


    retrieved_books = retrieve_books(
        preferred_genres=user_genre_preference,
        user_description=user_preference_description,
        excluded_genres=excluded_genres,
        excluded_authors=excluded_authors
    )

    books_for_llm = book_services.index_books_with_id_list(
        retrieved_books
    )

    recommended_books = recommend_books_with_llm(
        user_genre_preference=user_genre_preference,
        user_preference_description=user_preference_description,
        books=books_for_llm
    )

    return recommended_books