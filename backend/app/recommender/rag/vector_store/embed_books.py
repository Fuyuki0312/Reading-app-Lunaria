if __name__ == "__main__":

    from app.recommender.rag.vector_store.chroma import get_chroma_collection
    from app.services.book_services import get_book_services
    from app.recommender.rag.embedding.model import embed_books

    book_services = get_book_services()
    collection = get_chroma_collection()

    all_books = book_services.get_books_with_genres()


    embedded_books = embed_books(all_books)
    print("Books:", len(all_books))
    print("Embeddings shape:", embedded_books.shape)

    collection.upsert(
        ids=[
            f"book_{book['id']}"
            for book in all_books
        ],

        embeddings=embedded_books.tolist(),

        metadatas=[
            {
                "book_id": book["id"],
                "title": book["title"]
            }
            for book in all_books
        ]
    )