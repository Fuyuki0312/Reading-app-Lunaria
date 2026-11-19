from app.recommender.rag.embedding.model import embed_query
from app.recommender.rag.vector_store.chroma import get_chroma_collection
from app.config import Config
from time import perf_counter

collection = get_chroma_collection()


def retrieve_books(
    preferred_genres: list[str],
    user_description: str,
    top_k: int = Config().NUM_OF_BOOKS_RETURNED_FROM_RAG,
    excluded_authors: list[str] | None = None,
    excluded_genres: list[str] | None = None,
    timings: dict[str, float] | None = None
) -> list[dict]:

    step_start = perf_counter()

    # Embed query
    query_embedding = embed_query(
        preferred_genres,
        user_description
    )

    if timings is not None:
        timings["embedding_s"] = perf_counter() - step_start

    # Filter
    conditions = []

    if excluded_authors:
        conditions.append({
            "author": {"$nin": excluded_authors}
        })

    if excluded_genres:
        for genre in excluded_genres:
            conditions.append({
                "genres": {"$not_contains": genre}
            })

    if not conditions:
        where_filter = None
    elif len(conditions) == 1:
        where_filter = conditions[0] # There is only 1 condition
    else:
        where_filter = {"$and": conditions} # A book must satisfy all conditions, so "$and" should be used here


    # Search based on cosine similarity
    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=min(top_k, collection.count()),
        where=where_filter
    )

    retrieved_books = []

    for metadata, distance in zip(
        results["metadatas"][0],
        results["distances"][0]
    ):
        retrieved_books.append({
            "book_id": metadata["book_id"],
            "title": metadata["title"],
            "similarity": 1 - distance
        })

    return retrieved_books