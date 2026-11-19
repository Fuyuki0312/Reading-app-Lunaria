import asyncio

from app.model.llm_response import RecommendationForm
from app.recommender.rag.llm.llm_recommendation import recommend_books_with_llm
from app.recommender.rag.llm.intent_extraction import extract_intents
from app.recommender.rag.retrieval import retrieve_books
from app.recommender.rag.retrieval import match_entities
from app.services.book_services import get_book_services
from time import perf_counter


book_services = get_book_services()

async def recommend_books_with_rag(
        user_genre_preference: list[str],
        user_preference_description: str,
        timings: dict[str, float] | None = None # for measuring latency
) -> list[RecommendationForm]:
    """
    This function run in the below order:

    1. extract entities and extract intents (see more about "entities" in entity_matching.py)
    2. retrieve books
    2.1. index books with ids
    3. llm recommends books
    """

    pipeline_start = perf_counter() # for measuring latency

    step_start = perf_counter()

    # Extract intents
    intents = await extract_intents(
        user_description=user_preference_description,
        entities=match_entities(user_preference_description)
    )

    if timings is not None:
        timings["intent_extraction_s"] = perf_counter() - step_start


    excluded_genres = None
    excluded_authors = []

    # review intents and print WARNINGS (if any)
    if intents:

        for entity in intents["entities"]:

            if entity["intent"] == "exclude":

                if entity["type"] == "author":
                    excluded_authors.append(entity["name"])
                elif entity["type"] == "book":
                    print("WARNING: Detected disliked books in Qwen's intent extraction. "
                          "RAG does not exclude disliked books for the time being.")
                else:
                    print("WARNING: Detected unknown type of which intent is 'excluded' in Qwen's intent extraction.")

        if intents["excluded_genres"]:
            excluded_genres = intents["excluded_genres"]


    retrieved_books = await asyncio.to_thread(
        retrieve_books,
        preferred_genres=user_genre_preference,
        user_description=user_preference_description,
        excluded_genres=excluded_genres,
        excluded_authors=excluded_authors,
        timings=timings
    )

    books_for_llm = book_services.index_books_with_id_list(
        retrieved_books
    )

    step_start = perf_counter()
    recommended_books = await recommend_books_with_llm(
        user_genre_preference=user_genre_preference,
        user_preference_description=user_preference_description,
        books=books_for_llm
    )

    if timings is not None:
        timings["llm_rerank_s"] = perf_counter() - step_start
        timings["pipeline_total_s"] = perf_counter() - pipeline_start

    return recommended_books