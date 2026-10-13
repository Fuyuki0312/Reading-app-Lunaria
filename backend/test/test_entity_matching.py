from app.recommender.rag.retrieval import entity_matching
from pprint import pprint

# Use actual books from the database
book = entity_matching.all_books[0]
author = book["author"]
title = book["title"]

# Test 1: Recognize known entities
text = f"I love {title} by {author}."

matches = entity_matching.match_entities(text)

assert any(
    m["type"] == "author" and m["name"] == author
    for m in matches
)

assert any(
    m["type"] == "book" and m["name"] == title
    for m in matches
)

print("Test 1: PASSED")


# Test 2: Case-insensitive matching
matches = entity_matching.match_entities(author.swapcase())

assert any(
    m["type"] == "author" and m["name"] == author
    for m in matches
)

print("Test 2: PASSED")


# Test 3: Do not match part of a longer word
matches = entity_matching.match_entities(author + "xyz")

assert not any(
    m["type"] == "author" and m["name"] == author
    for m in matches
)

print("Test 3: PASSED")


# Test 4: Check character offsets
text = f"I love {author}."
matches = entity_matching.match_entities(text)

author_match = next(
    m for m in matches
    if m["type"] == "author" and m["name"] == author
)

assert text[
    author_match["start"]:author_match["end"]
] == author

print("Test 4: PASSED")


# Test 5: Check cache reuse
cached_entities = entity_matching.entities

for _ in range(100):
    entity_matching.match_entities(text)

assert entity_matching.entities is cached_entities

print("Test 5: PASSED")


# Visualization
text = "I love Iris Vale, but I prefer Nora Vale."
results = entity_matching.match_entities(text)
pprint(results)