from app.database.database import get_cursor_from_database, get_database

import json


database = get_database()
cursor = get_cursor_from_database()

class UserService:


    # Registeration ----------------------------------------

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


    def register_preference_description_to_database(
            self,
            username,
            description
    ):

        cursor.execute(f"""
            UPDATE users
            SET preference_description = %s
            WHERE username = %s
        """, (
            description,
            username
        ))

        database.commit()


    # Getter from database ----------------------------------

    def get_genre_preferences_from_username(self, username):

        cursor.execute(f"""
            SELECT genre_preferences FROM users
            WHERE username = %s;
        """, (
            username,
        ))

        result_from_database = cursor.fetchone()
        return result_from_database["genre_preferences"]

    def get_preference_description_from_username(self, username):

        cursor.execute(f"""
            SELECT preference_description FROM users
            WHERE username = %s;
        """, (
            username,
        ))

        result_from_database = cursor.fetchone()

        return result_from_database["preference_description"]


    def get_all_username_from_database(self):

        cursor.execute(f"""
            SELECT username FROM users;
        """)

        username_list = cursor.fetchall()
        return username_list


    def get_password_by_username_from_database(self, username):

        cursor.execute(f"""
            SELECT insecured_password FROM users
            WHERE username = %s;
        """, (
            username,
        ))

        result_from_database = cursor.fetchone()
        return result_from_database["insecured_password"]


user_services = UserService()

def get_user_services():

    return user_services