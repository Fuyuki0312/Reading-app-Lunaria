from app.recommender.baseline.baseline import Baseline
from metric_calculator import normalized_dcg, normalized_precision, violation_rate
from app.recommender.rag.llm.recommendation import recommend_books
from app.config import Config

import json
import pandas as pd


config = Config()

def save_metrics_per_user_to_csv(one_user_metric_results: list[dict]):
    df = pd.DataFrame(one_user_metric_results)
    df.to_csv(
        "eval_results/per_user_metrics.csv",
        index=True
    )


def save_mean_metrics_to_csv(one_user_metric_results: list[dict]):

    k = len(one_user_metric_results)

    LLM_ndcg_in_total = 0
    LLM_precision_in_total = 0
    LLM_violation_rate_in_total = 0

    Baseline_ndcg_in_total = 0
    Baseline_precision_in_total = 0
    Baseline_violation_rate_in_total = 0

    for row in one_user_metric_results:
        LLM_ndcg_in_total += row["LLM_ndcg"]
        LLM_precision_in_total += row["LLM_precision"]
        LLM_violation_rate_in_total += row["LLM_violation_rate"]

        Baseline_ndcg_in_total += row["Baseline_ndcg"]
        Baseline_precision_in_total += row["Baseline_precision"]
        Baseline_violation_rate_in_total += row["Baseline_violation_rate"]

    LLM_ndcg_mean = LLM_ndcg_in_total / k
    LLM_precision_mean = LLM_precision_in_total / k
    LLM_violation_rate_mean = LLM_violation_rate_in_total / k

    Baseline_ndcg_mean = Baseline_ndcg_in_total / k
    Baseline_precision_mean = Baseline_precision_in_total / k
    Baseline_violation_rate_mean = Baseline_violation_rate_in_total / k

    table = [
        {
            "LLM_ndcg_mean": LLM_ndcg_mean,
            "LLM_precision_mean": LLM_precision_mean,
            "LLM_violation_rate_mean": LLM_violation_rate_mean,
            "Baseline_ndcg_mean": Baseline_ndcg_mean,
            "Baseline_precision_mean": Baseline_precision_mean,
            "Baseline_violation_rate_mean": Baseline_violation_rate_mean
        }
    ]

    df = pd.DataFrame(table)
    df.to_csv(
        "eval_results/mean_metrics.csv",
        index=False
    )


# Get dataset -----------------------------------------------


with open("eval_dataset\\eval_users.json") as f:
    eval_users = json.load(f)

with open("eval_dataset\\relevance_labels.json") as f:
    eval_relevance = json.load(f)


# Baseline initialization -----------------------------------

baseline = Baseline()

# Search for all fake users ---------------------------------

number_of_books = int(len(eval_relevance) / len(eval_users))

eval_results: list[dict[str, float]] = [ # Below is an example of what will be stored in this variable
    #{
        # "LLM_ndcg" : 0.85,
        # "LLM_precision": 0.80,
        # "LLM_violation_rate": 0.30,
        # "Baseline_ndcg": 0.62,
        # "Baseline_precision": 0.80,
        # "Baseline_violation_rate": 0.71
    #}
] # to be transfered to panda DataFrame and to be stored as csv

for user in eval_users:

    print(f"Recommending books for user {user['id']}...\n")

    # Get recommendations from LLM and from baseline

    baseline_recommended_books = baseline.score_books(
        user_genre_preferences=user["genre_preferences"]
    )

    llm_recommeded_books = recommend_books(
        user_genre_preference=user["genre_preferences"],
        user_preference_description=user["genre_description"]
    )

    # Get ideal recommendations

    user_id = user["id"]
    ideal_recommended_books_in_order = []


    relevance_start_idx = number_of_books * (user_id - 1)
    relevance_end_idx = relevance_start_idx + number_of_books

    assert type(relevance_start_idx) is int, "relevance_start_idx is NOT int, check relevance_start_idx's equation"
    assert type(relevance_end_idx) is int, "relevance_end_idx is NOT int, check relevance_end_idx's equation"

    book_id_with_relevance_score: dict[int, dict] = {} # book_id: {"rel_score": rel_score,
                                                       #           "violation": bool},
    for i in range(relevance_start_idx, relevance_end_idx):
        ideal_recommended_books_in_order.append(
            {
                "book_id": eval_relevance[i]["book_id"],
                "relevance": eval_relevance[i]["relevance"]
            }
        )

        book_id_with_relevance_score[eval_relevance[i]["book_id"]] = {
            "rel_score": eval_relevance[i]["relevance"],
            "violation": eval_relevance[i]["violation"]
        }

    ideal_recommended_books_in_order.sort(key=lambda x: x["relevance"], reverse=True)

    ideal_recommended_books_in_order = ideal_recommended_books_in_order[:config.NUM_OF_RECOMMENDED_BOOK]

    # Get relevance score and violation rate from each method's recommendations

    ideal_rel_in_order = []
    for book_rel in ideal_recommended_books_in_order:
        ideal_rel_in_order.append(book_rel["relevance"])

    llm_rel_in_order = []
    llm_violaion_counter = 0
    for book in llm_recommeded_books:
        book_id = book["book_id"]
        rel = book_id_with_relevance_score[book_id]["rel_score"]

        if book_id_with_relevance_score[book_id]["violation"]:
            llm_violaion_counter += 1

        llm_rel_in_order.append(rel)


    baseline_rel_in_order = []
    baseline_violation_counter = 0
    for book in baseline_recommended_books:
        book_id = book["book_id"]
        rel = book_id_with_relevance_score[book_id]["rel_score"]

        if book_id_with_relevance_score[book_id]["violation"]:
            baseline_violation_counter += 1

        baseline_rel_in_order.append(rel)


    # Calculate metrics and round to ?four? decimal places (example: 0.8234)

    max_num_of_relevant_book = sum(
        rel >= config.RELEVANCE_THRESHOLD
        for rel in ideal_rel_in_order
    )

    llm_ndcg = round(normalized_dcg(
        llm_rel_in_order,
        ideal_rel_in_order
    ), config.NUM_DIGITS_ROUNDED_FOR_METRICS)

    llm_precision = round(
        normalized_precision(llm_rel_in_order, config.RELEVANCE_THRESHOLD, max_num_of_relevant_book),
        config.NUM_DIGITS_ROUNDED_FOR_METRICS
    )

    llm_violation_rate = round(
        violation_rate(llm_violaion_counter, len(llm_recommeded_books)),
        config.NUM_DIGITS_ROUNDED_FOR_METRICS
    )


    baseline_ndcg = round(normalized_dcg(
        baseline_rel_in_order,
        ideal_rel_in_order
    ), config.NUM_DIGITS_ROUNDED_FOR_METRICS)

    baseline_precision = round(
        normalized_precision(baseline_rel_in_order, config.RELEVANCE_THRESHOLD, max_num_of_relevant_book),
        config.NUM_DIGITS_ROUNDED_FOR_METRICS
    )

    baseline_violation_rate = round(
        violation_rate(baseline_violation_counter, len(baseline_recommended_books)),
        config.NUM_DIGITS_ROUNDED_FOR_METRICS
    )

    # Process metrics to store them as .csv

    eval_results.append(
        {
            "user_id": user_id,
            "LLM_ndcg": llm_ndcg,
            "LLM_precision": llm_precision,
            "LLM_violation_rate": llm_violation_rate,
            "Baseline_ndcg": baseline_ndcg,
            "Baseline_precision": baseline_precision,
            "Baseline_violation_rate": baseline_violation_rate
        }
    )

    print(f"LLM_ndcg: {llm_ndcg}")
    print(f"LLM_precision: {llm_precision}")
    print(f"LLM_violation_rate: {llm_violation_rate}")
    print()
    print(f"Baseline_ndcg: {baseline_ndcg}")
    print(f"Baseline_precision: {baseline_precision}")
    print(f"Baseline_violation_rate: {baseline_violation_rate}")
    print()
    print()

save_metrics_per_user_to_csv(eval_results)
save_mean_metrics_to_csv(eval_results)


