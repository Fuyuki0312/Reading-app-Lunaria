import re

from app.services.book_services import BookServices

book_services = BookServices()
all_books = book_services.get_books_with_genres()


entities = set()

for book in all_books:
    entities.add(("author", book["author"]))
    entities.add(("book", book["title"]))


def match_entities(
    user_description: str
) -> list[dict]:

    global entities

    matches = []

    for entity_type, name in entities:

        pattern = rf"(?<!\w){re.escape(name)}(?!\w)"

        for match in re.finditer(
            pattern,
            user_description,
            flags=re.IGNORECASE
        ):
            matches.append({
                "type": entity_type,
                "name": name,
                "start": match.start(),
                "end": match.end()
            })

    return sorted(matches, key=lambda x: x["start"])