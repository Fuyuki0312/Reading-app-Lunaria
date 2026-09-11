from app.recommender.semantic.llm.recommendation import recommend_books

print(recommend_books(
    user_genre_preference=["Fantasy"]
))