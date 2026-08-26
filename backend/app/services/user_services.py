from app.database.database import get_cursor_from_database, get_database

import json


database = get_database()
cursor = get_cursor_from_database()

class UserService:

    def register_user_account_to_database(
            self,
            username: str,
            password: str,
            genre_preferences: list
    ):
        cursor.execute(f"""
            INSERT INTO users(username, insecured_password, genre_preferences)
            VALUES (%s, %s, %s);
            """, (
            username,
            password,
            json.dumps(genre_preferences)
        ))

        database.commit()

    def register_genre_preferences_to_database(
            self,
            preferences: list,
            username: str
    ):

        cursor.execute(f"""
            UPDATE users
            SET genre_preferences = %s
            WHERE username = %s;
        """, (
            json.dumps(preferences),
            username
        ))
        database.commit()


    def get_genre_preferences_from_username(self, username):

        cursor.execute(f"""
            SELECT genre_preferences FROM users
            WHERE username = %s;
        """, (
            username,
        ))

        result_from_database = cursor.fetchone()
        return result_from_database["genre_preferences"]


user_services = UserService()

def get_user_services():

    return user_services