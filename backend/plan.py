# TODO: learn tools:
#  - (DONE) Use LangChain (to explore different LLMs and to ensure JSON-structured outputs)
#  - Use Docker (I don't know why. Job description wants it, but I will research later if I really need it.)

# TODO depth:
#  - Explore more LLM options
#  - Test Lunaria with a large number of users
#  - Help RAG handle users writting explicit names (author, book titles) in free-text description
#  - (Optional) expand eval dataset or database
#  LEGENDARY QUEST ✨: Continual Learning

# TODO breadth:
#  - (DONE) Enable users to actually read books
#  - Hash users' password
#  - Style: Decorate app with Lunaria style
#  - Use something to do Semantic Search
#  - Add settings: enable users to configure font size, background color (maybe I need something to store user's settings)

from app.recommender.rag.retrieval import retrieve_books
from app.services.book_services import get_book_services

results = retrieve_books(
    preferred_genres=["Mystery"],
    user_description="I enjoy mysterious stories.",
    excluded_authors=["Iris Vale"],
    excluded_genres=["Dark Fantasy", "Psychological Thriller"]
)

books = get_book_services().index_books_with_id_list(results)

for book in books:
    assert book["author"] != "Iris Vale"
    assert "Dark Fantasy" not in book["genres"]
    assert "Psychological Thriller" not in book["genres"]

print("Retrieved:", len(books))
print("Pre-filtered semantic retrieval: PASSED")