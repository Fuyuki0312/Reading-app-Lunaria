from app.config import Config

from sentence_transformers import SentenceTransformer


config = Config()
model = SentenceTransformer(config.EMBEDDING_MODEL)


def embed_query(preferred_genres: list[str], user_description: str):

    genres = ", ".join(preferred_genres)
    query_text = (
        f"query: "
        f"Genres: {genres}. "
        f"{user_description}"
    )
    return model.encode(query_text, normalize_embeddings=True)


def embed_books(all_books: list[dict]):
    book_texts = [
        (
            f"passage: "
            f"Genres: {', '.join(book['genres'])}. "
            f"{book['description'] or ''}"
        )
        for book in all_books
    ]

    return model.encode(book_texts, normalize_embeddings=True)