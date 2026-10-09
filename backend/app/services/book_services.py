from app.database.database import get_database_connection

import json
import copy

from app.model.llm_response import RecommendationForm


class BookServices:

    def __init__(self):

        database = get_database_connection()
        cursor = database.cursor(
            dictionary=True
        )

        try:
            # Create a list of books' id with their genres ---------
            cursor.execute("""
                SELECT b.id, g.name
                FROM books b
                JOIN book_genres bg
                    ON bg.book_id = b.id
                JOIN genres g
                    ON bg.genre_id = g.id;
            """)

            self.books_id_with_genres = cursor.fetchall()


            cursor.execute("SELECT * FROM books")
            self.books_without_genres = cursor.fetchall()

            self.books = copy.deepcopy(self.books_without_genres)

            self.attach_genres_to_books() # self.books become a list of books with their genres

        finally:

            cursor.close()
            database.close()


    def attach_genres_to_books(self):

        hash_map_of_book_id_and_index = {}


        for i, book in enumerate(self.books):
            hash_map_of_book_id_and_index[book["id"]] =  i

            self.books[i].pop("cover_path")  # I don't want the model to see cover_path
            self.books[i]["genres"] = []


        for book_id_with_genre in self.books_id_with_genres:

            pos_of_book_in_database = hash_map_of_book_id_and_index[book_id_with_genre["id"]]
            self.books[pos_of_book_in_database]["genres"].append(book_id_with_genre["name"])


    def get_books_with_genres(self) -> list:

        return copy.deepcopy(self.books)


    def index_books_with_id_list(self, list_of_book_id: list) -> list[dict]:

        indexed_books = []

        for recommended_form in list_of_book_id:

            if isinstance(recommended_form, dict):
                id = recommended_form["book_id"]
            elif isinstance(recommended_form, RecommendationForm):
                id = recommended_form.book_id
            else:
                raise Exception("Book service cannot recognize what is in list_of_book_id.")

            for book in self.books:
                if id == book["id"]:
                    indexed_books.append(book)
                    break

        return indexed_books


    def get_the_number_of_books_in_database(self) -> int:

        return len(self.books)


    def get_pages_by_book_id(self, book_id: int):

        database = get_database_connection()
        cursor = database.cursor(
            dictionary=True
        )

        try:
            cursor.execute("""
                SELECT page_num, book_id, content
                FROM pages
                WHERE book_id = %s
                ORDER BY page_num
            """, (book_id,))

            rows = cursor.fetchall()
            pages = []

            # the for loop below ensures this function returns the type which frontend expects
            for row in rows:

                content = row["content"]

                if isinstance(content, str):
                    content = json.loads(content)

                pages.append({
                    "page_num": row["page_num"],
                    "book_id": row["book_id"],
                    "content": content
                })

            return pages

        finally:

            cursor.close()
            database.close()

book_services = BookServices()

def get_book_services():

    return book_services