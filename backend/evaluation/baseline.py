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
from app.services.book_services import get_book_services


import random


config = Config()
book_services = get_book_services()

class Baseline:

    def __init__(self):
        self.all_book_genres = book_services.get_books_with_genres()
        self.score_table = []

        for book in self.all_book_genres:
            book["score"] = 0

        random.shuffle(self.all_book_genres)


    def score_books(self, user_genre_preferences: list[str]) -> list[dict[str, int]]:

        user_genre_preferences_set = set()
        for genre in user_genre_preferences:
            user_genre_preferences_set.add(genre)

        for book in self.all_book_genres:

            for genre in book["genres"]:

                if genre in user_genre_preferences_set:
                    book["score"] += 1

        self.all_book_genres.sort(key=lambda x: x["score"], reverse=True)

        return self.recommend_book_id()


    def recommend_book_id(self) -> list[dict[str, int]]:

        recommended_id_list = []

        for i in range(config.NUM_OF_RECOMMENDED_BOOK):

            recommended_id_list.append(
                {"id": self.all_book_genres[i]["id"]}
            )

        return recommended_id_list
