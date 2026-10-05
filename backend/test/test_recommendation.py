from app.recommender.rag.llm.recommendation import recommend_books

import json

with open("books.json", "r") as f:

    books = json.load(f)

print(recommend_books(
    user_genre_preference=["Fantasy", "Mystery"],
    user_preference_description="None",
    books=books
))

