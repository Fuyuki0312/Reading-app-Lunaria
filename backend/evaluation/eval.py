from baseline import Baseline
from metric_calculator import normalized_dcg
from app.ai.recommendation import recommend_books
from app.config import Config

import json


config = Config()

# Get dataset -----------------------------------------------


with open("eval_dataset\\eval_users.json") as f:
    eval_users = json.load(f)

with open("eval_dataset\\relevance_labels.json") as f:
    eval_relevance = json.load(f)


# Baseline initialization -----------------------------------

baseline = Baseline()

# Search for all fake users ---------------------------------

number_of_books = int(len(eval_relevance) / len(eval_users))

for user in eval_users:

    baseline_recommended_books = baseline.score_books(
        user_genre_preferences=user["genre_preferences"]
    )

    llm_recommeded_books = recommend_books(
        user_genre_preference=user["genre_preferences"],
        user_preference_description=user["genre_description"]
    )

    user_id = user["id"]
    ideal_recommended_books_in_order = []


    relevance_start_idx = number_of_books * (user_id - 1)
    relevance_end_idx = relevance_start_idx + number_of_books

    assert type(relevance_start_idx) is int, "relevance_start_idx is NOT int, check relevance_start_idx's equation"
    assert type(relevance_end_idx) is int, "relevance_end_idx is NOT int, check relevance_end_idx's equation"

    book_id_with_relevance_score: dict[int, int] = {} # {1: 3} # book_id: relevance_score
    for i in range(relevance_start_idx, relevance_end_idx):
        ideal_recommended_books_in_order.append(
            {
                "book_id": eval_relevance[i]["book_id"],
                "relevance": eval_relevance[i]["relevance"]
            }
        )
        book_id_with_relevance_score[eval_relevance[i]["book_id"]] = eval_relevance[i]["relevance"]

    ideal_recommended_books_in_order.sort(key=lambda x: x["relevance"], reverse=True)

    ideal_recommended_books_in_order = ideal_recommended_books_in_order[:config.NUM_OF_RECOMMENDED_BOOK]


    ideal_rel_in_order = []
    for book_rel in ideal_recommended_books_in_order:
        ideal_rel_in_order.append(book_rel["relevance"])

    llm_rel_in_order = []
    for book in llm_recommeded_books:
        book_id = book["book_id"]
        rel = book_id_with_relevance_score[book_id]
        llm_rel_in_order.append(rel)

    baseline_rel_in_order = []
    for book in baseline_recommended_books:
        rel = book_id_with_relevance_score[book["id"]]
        baseline_rel_in_order.append(rel)


    llm_ndcg = normalized_dcg(
        llm_rel_in_order,
        ideal_rel_in_order
    )

    baseline_ndcg = normalized_dcg(
        baseline_rel_in_order,
        ideal_rel_in_order
    )
    # TODO: display ndcg and store it somewhere