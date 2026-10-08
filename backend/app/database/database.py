from pathlib import Path
from dotenv import load_dotenv
import os
from mysql.connector.pooling import MySQLConnectionPool


ENV_PATH = Path(__file__).resolve().parents[1] / ".env"

load_dotenv(
    dotenv_path=ENV_PATH,
    override=True
)


MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


database_pool = MySQLConnectionPool(
    pool_name="lunaria_pool",
    pool_size=5,

    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE,
    use_pure=True
)


def get_database_connection():

    return database_pool.get_connection()