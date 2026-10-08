"""
Baseline will recommend books for users
only based on books' genres
and users' genre_preferences

How baseline recommends books:
- Books are scored based on how many genres they match user_preferences
- Based-on scores, baseline choose the highest books.
  If there are books that have equivalient scores, they will be chosen randomly


* sample:

all_book_genres = [
    {
        "id": 1,
        "genres": ["Fantasy", "Adventure"]
    }
]
"""

from app.config import Config
from app.model.llm_response import RecommendationForm
from app.services.book_services import get_book_services


import random


config = Config()
random.seed(config.RANDOM_SEED)
book_services = get_book_services()

class Baseline:

    def __init__(self):
        self.all_book_genres = book_services.get_books_with_genres()
        self.score_table = []

        for book in self.all_book_genres:
            book["score"] = 0

        random.shuffle(self.all_book_genres)


    def score_books(self, user_genre_preferences: list[str]) -> list[RecommendationForm]:

        user_genre_preferences_set = set()
        for genre in user_genre_preferences:
            user_genre_preferences_set.add(genre)

        for book in self.all_book_genres:
            book["score"] = 0
            for genre in book["genres"]:

                if genre in user_genre_preferences_set:
                    book["score"] += 1

        self.all_book_genres.sort(key=lambda x: x["score"], reverse=True)

        return self.recommend_book_id() # return example: see the return type


    def recommend_book_id(self) -> list[RecommendationForm]:

        recommended_id_list = []

        for i in range(config.NUM_OF_RECOMMENDED_BOOK):

            recommended_id_list.append(
                #{"book_id": self.all_book_genres[i]["id"]}
                RecommendationForm(
                    book_id=self.all_book_genres[i]["id"],
                    reason=f"score: {self.all_book_genres[i]['score']}"
                )
            )

        return recommended_id_list
