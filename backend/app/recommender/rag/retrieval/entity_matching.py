# This is called Regular Expression (Regex)

# This will find all author names and book titles inside
# user text-free description (if there are any)

import re

from app.services.book_services import get_book_services

book_services = get_book_services()
all_books = book_services.get_books_with_genres()


entities = set()

for book in all_books:
    entities.add(("author", book["author"]))
    entities.add(("book", book["title"]))


def match_entities(
    user_description: str
) -> list[dict]: # see return example down below

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

    # return example:

    # [{'end': 16, 'name': 'Iris Vale', 'start': 7, 'type': 'author'},
    #  {'end': 40, 'name': 'Nora Vale', 'start': 31, 'type': 'author'}]