from pathlib import Path
from dotenv import load_dotenv
import os
import mysql.connector


ENV_PATH = Path(__file__).resolve().parents[1] / ".env"

load_dotenv(
    dotenv_path=ENV_PATH,
    override=True
)


MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


database = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE,
    use_pure=True
)

cursor = database.cursor(dictionary=True)


def get_cursor_from_database():

    return cursor

def get_database():

    return database