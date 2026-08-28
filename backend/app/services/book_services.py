from app.database.database import get_cursor_from_database


cursor = get_cursor_from_database()

class BookServices:

    def __init__(self):

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

        self.books = self.books_without_genres.copy()

        self.attach_genres_to_books() # self.books become a list of books with their genres



    def attach_genres_to_books(self):

        hash_map_of_book_id_and_index = {}


        for i, book in enumerate(self.books):
            hash_map_of_book_id_and_index[book["id"]] =  i

            self.books[i].pop("cover_path")  # I don't want the model to see cover_path
            self.books[i]["genres"] = []


        for book_id_with_genre in self.books_id_with_genres:

            pos_of_book_in_database = hash_map_of_book_id_and_index[book_id_with_genre["id"]]
            self.books[pos_of_book_in_database]["genres"].append(book_id_with_genre["name"])


    def get_books_with_genres(self):

        return self.books


    def index_books_with_id_list(self, list_of_book_id):

        indexed_books = []

        for recommended_id in list_of_book_id:
            id = recommended_id["book_id"]

            for book in self.books:
                if id == book["id"]:
                    indexed_books.append(book)
                    break

        return indexed_books


book_services = BookServices()

def get_book_services():

    return book_services