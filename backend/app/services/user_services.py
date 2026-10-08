from app.database.database import get_database_connection

import json



class UserService:


    # Registeration ----------------------------------------

    def register_user_account_to_database(
            self,
            username: str,
            password: str,
            genre_preferences: list
    ):

        database = get_database_connection()
        cursor = database.cursor(dictionary=True)

        try:
            cursor.execute(f"""
                INSERT INTO users(username, insecured_password, genre_preferences)
                VALUES (%s, %s, %s);
                """, (
                username,
                password,
                json.dumps(genre_preferences)
            ))

            database.commit()

        finally:

            cursor.close()
            database.close()


    def register_genre_preferences_to_database(
            self,
            preferences: list,
            username: str
    ):

        database = get_database_connection()
        cursor = database.cursor(dictionary=True)

        try:
            cursor.execute(f"""
                UPDATE users
                SET genre_preferences = %s
                WHERE username = %s;
            """, (
                json.dumps(preferences),
                username
            ))
            database.commit()

        finally:

            cursor.close()
            database.close()


    def register_preference_description_to_database(
            self,
            username,
            description
    ):

        database = get_database_connection()
        cursor = database.cursor(dictionary=True)

        try:

            cursor.execute(f"""
                UPDATE users
                SET preference_description = %s
                WHERE username = %s
            """, (
                description,
                username
            ))

            database.commit()

        finally:

            cursor.close()
            database.close()


    # Getter from database ----------------------------------

    def get_genre_preferences_from_username(self, username):

        database = get_database_connection()
        cursor = database.cursor(dictionary=True)

        try:
            cursor.execute(f"""
                SELECT genre_preferences FROM users
                WHERE username = %s;
            """, (
                username,
            ))

            result_from_database = cursor.fetchone()
            genre_preferences = json.loads(result_from_database["genre_preferences"])
            return genre_preferences

        finally:

            cursor.close()
            database.close()

    def get_preference_description_from_username(self, username):

        database = get_database_connection()
        cursor = database.cursor(dictionary=True)

        try:
            cursor.execute(f"""
                SELECT preference_description FROM users
                WHERE username = %s;
            """, (
                username,
            ))

            result_from_database = cursor.fetchone()

            return result_from_database["preference_description"]

        finally:

            cursor.close()
            database.close()

    def get_all_username_from_database(self):

        database = get_database_connection()
        cursor = database.cursor(dictionary=True)

        try:
            cursor.execute(f"""
                SELECT username FROM users;
            """)

            username_list = cursor.fetchall()
            return username_list

        finally:

            cursor.close()
            database.close()


    def get_password_by_username_from_database(self, username):

        database = get_database_connection()
        cursor = database.cursor(dictionary=True)

        try:

            cursor.execute(f"""
                SELECT insecured_password FROM users
                WHERE username = %s;
            """, (
                username,
            ))

            result_from_database = cursor.fetchone()
            return result_from_database["insecured_password"]

        finally:

            cursor.close()
            database.close()

user_services = UserService()

def get_user_services():

    return user_services