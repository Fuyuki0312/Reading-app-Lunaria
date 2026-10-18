from app.model.username import Username
from app.recommender.rag.llm.llm_recommendation import recommend_books_with_llm
from app.api.router import recommend

import json

with open("books.json", "r") as f:

    books = json.load(f)

print(recommend_books_with_llm(
    user_genre_preference=["Fantasy", "Mystery"],
    user_preference_description="None",
    books=books
))

print(recommend(Username(username="testRaG")))
