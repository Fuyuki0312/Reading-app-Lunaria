import mysql.connector
import json

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ultimate0312@",
    database="lunaria"
)

cursor = database.cursor(dictionary=True)

cursor.execute("SELECT * FROM pages")
books = cursor.fetchall()
print(books)

for i, page in enumerate(books):

    books[i]["content"] = json.loads(page["content"])


with open("books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=4)

