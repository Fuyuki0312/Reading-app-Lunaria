from app.recommender.rag.embedding.model import embed_query
from app.recommender.rag.vector_store.chroma import get_chroma_collection
from app.config import Config


config = Config()

def retrieve_books(
    preferred_genres: list[str],
    user_description: str,
    top_k: int = config.NUM_OF_BOOKS_RETURNED_FROM_RAG
) -> list[dict]:
    query_embedding = embed_query(
        preferred_genres,
        user_description
    )

    collection = get_chroma_collection()

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=min(top_k, collection.count())
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