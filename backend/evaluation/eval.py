from app.recommender.baseline.baseline import Baseline
from app.recommender.rag.retrieval import retrieve_books
from app.services.book_services import get_book_services
from metric_calculator import normalized_dcg, normalized_precision, violation_rate
from app.recommender.rag.llm.recommendation import recommend_books
from app.config import Config

import torch
import json
import pandas as pd


config = Config()
book_services = get_book_services()
torch.manual_seed(config.TORCH_SEED)




# Save functions

def save_metrics_per_user_to_csv(one_user_metric_results: list[dict]):
    df = pd.DataFrame(one_user_metric_results)
    df.to_csv(
        "eval_results/genre_match_priority/per_user_metrics.csv",
        index=False
    )


def save_mean_metrics_to_csv(one_user_metric_results: list[dict]):

    k = len(one_user_metric_results)

    LLM_ndcg_in_total = 0
    LLM_precision_in_total = 0
    LLM_violation_rate_in_total = 0

    Baseline_ndcg_in_total = 0
    Baseline_precision_in_total = 0
    Baseline_violation_rate_in_total = 0

    RAG_ndcg_in_total = 0
    RAG_precision_in_total = 0
    RAG_violation_rate_in_total = 0

    for row in one_user_metric_results:
        LLM_ndcg_in_total += row["LLM_ndcg"]
        LLM_precision_in_total += row["LLM_precision"]
        LLM_violation_rate_in_total += row["LLM_violation_rate"]

        Baseline_ndcg_in_total += row["Baseline_ndcg"]
        Baseline_precision_in_total += row["Baseline_precision"]
        Baseline_violation_rate_in_total += row["Baseline_violation_rate"]

        RAG_ndcg_in_total += row["RAG_ndcg"]
        RAG_precision_in_total += row["RAG_precision"]
        RAG_violation_rate_in_total += row["RAG_violation_rate"]

    LLM_ndcg_mean = LLM_ndcg_in_total / k
    LLM_precision_mean = LLM_precision_in_total / k
    LLM_violation_rate_mean = LLM_violation_rate_in_total / k

    Baseline_ndcg_mean = Baseline_ndcg_in_total / k
    Baseline_precision_mean = Baseline_precision_in_total / k
    Baseline_violation_rate_mean = Baseline_violation_rate_in_total / k

    RAG_ndcg_mean = RAG_ndcg_in_total / k
    RAG_precision_mean = RAG_precision_in_total / k
    RAG_violation_rate_mean = RAG_violation_rate_in_total / k

    table = [
        {
            "LLM_ndcg_mean": LLM_ndcg_mean,
            "LLM_precision_mean": LLM_precision_mean,
            "LLM_violation_rate_mean": LLM_violation_rate_mean,
            "Baseline_ndcg_mean": Baseline_ndcg_mean,
            "Baseline_precision_mean": Baseline_precision_mean,
            "Baseline_violation_rate_mean": Baseline_violation_rate_mean,
            "RAG_ndcg_mean": RAG_ndcg_mean,
            "RAG_precision_mean": RAG_precision_mean,
            "RAG_violation_rate_mean": RAG_violation_rate_mean
        }
    ]

    df = pd.DataFrame(table)
    df.to_csv(
        "eval_results/genre_match_priority/mean_metrics.csv",
        index=False
    )


def save_books_recommeded_by_llm(recommendations_from_llm):

    with open("eval_results\\genre_match_priority\\analysis\\books_from_llm.json", "w") as file:
        json.dump(recommendations_from_llm, file, indent=4)


def save_books_recommeded_by_rag(recommendations_from_rag):

    with open("eval_results\\genre_match_priority\\analysis\\books_from_rag.json", "w") as file:
        json.dump(recommendations_from_rag, file, indent=4)


def save_books_recommeded_by_embedding_model(recommendations_from_embedding_model):

    with open("eval_results\\genre_match_priority\\analysis\\books_from_embedding_model.json", "w") as file:
        json.dump(recommendations_from_embedding_model, file, indent=4)


# Get dataset -----------------------------------------------


with open("eval_dataset\\eval_users.json", "r") as f:
    eval_users = json.load(f)

with open("eval_dataset\\genre_match_priority_relevance\\relevance_labels.json", "r") as f:
    eval_relevance = json.load(f)


# Baseline initialization -----------------------------------

baseline = Baseline()

# Search for all fake users ---------------------------------

number_of_books = int(len(eval_relevance) / len(eval_users))

eval_results: list[dict[str, float]] = [
    # Below is an example of what will be stored in this variable
    #{
        # "LLM_ndcg" : 0.85,
        # "LLM_precision": 0.80,
        # "LLM_violation_rate": 0.30,
        # "Baseline_ndcg": 0.62,
        # "Baseline_precision": 0.80,
        # "Baseline_violation_rate": 0.71,
        # "RAG_ndcg": ...,
        # "RAG_precision": ...,
        # "RAG_violation_rate": ...
    #}
] # to be transfered to panda DataFrame and to be stored as csv


all_recommendations_from_llm = []
all_recommendations_from_rag = []
all_recommendations_from_embedding_model = []

def main():

    for user in eval_users:

        print(f"Recommending books for user {user['id']}...\n")

        # Get recommendations from baseline

        baseline_recommended_books = baseline.score_books(
            user_genre_preferences=user["genre_preferences"]
        )

        # Get recommendations from LLM

        llm_recommeded_books = recommend_books(
            user_genre_preference=user["genre_preferences"],
            user_preference_description=user["genre_description"],
            books=book_services.get_books_with_genres()
        )

        all_recommendations_from_llm.append(
            {
                "user_id": user["id"],
                "recommendations": llm_recommeded_books
            }
        )

        # Get recommendations from RAG

        retrieved_books = retrieve_books(
            preferred_genres=user["genre_preferences"],
            user_description=user["genre_description"]
        )

        all_recommendations_from_embedding_model.append(
            {
                "user_id": user["id"],
                "recommendations": retrieved_books
            }
        )

        books_for_llm_with_rag = book_services.index_books_with_id_list(
            retrieved_books
        )

        rag_recommeded_books = recommend_books(
            user_genre_preference=user["genre_preferences"],
            user_preference_description=user["genre_description"],
            books=books_for_llm_with_rag
        )

        all_recommendations_from_rag.append(
            {
                "user_id": user["id"],
                "recommendations": rag_recommeded_books
            }
        )

        # Get ideal recommendations

        user_id = user["id"]
        ideal_recommended_books_in_order = []


        relevance_start_idx = number_of_books * (user_id - 1)
        relevance_end_idx = relevance_start_idx + number_of_books

        assert type(relevance_start_idx) is int, "relevance_start_idx is NOT int, check relevance_start_idx's equation"
        assert type(relevance_end_idx) is int, "relevance_end_idx is NOT int, check relevance_end_idx's equation"

        book_id_with_relevance_score: dict[int, dict] = {} # = {"rel_score": rel_score,
                                                           #    "violation": bool},
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

            # Ideal
        ideal_rel_in_order = []
        for book_rel in ideal_recommended_books_in_order:
            ideal_rel_in_order.append(book_rel["relevance"])

            # LLM only
        llm_rel_in_order = []
        llm_violaion_counter = 0
        for book in llm_recommeded_books:
            book_id = book["book_id"]
            rel = book_id_with_relevance_score[book_id]["rel_score"]

            if book_id_with_relevance_score[book_id]["violation"]:
                llm_violaion_counter += 1

            llm_rel_in_order.append(rel)

            # RAG
        rag_rel_in_order = []
        rag_violation_counter = 0
        for book in rag_recommeded_books:
            book_id = book["book_id"]
            rel = book_id_with_relevance_score[book_id]["rel_score"]

            if book_id_with_relevance_score[book_id]["violation"]:
                rag_violation_counter += 1

            rag_rel_in_order.append(rel)


            # Baseline
        baseline_rel_in_order = []
        baseline_violation_counter = 0
        for book in baseline_recommended_books:
            book_id = book["book_id"]
            rel = book_id_with_relevance_score[book_id]["rel_score"]

            if book_id_with_relevance_score[book_id]["violation"]:
                baseline_violation_counter += 1

            baseline_rel_in_order.append(rel)


        # Calculate precisions and round them to four decimal places (example: 0.1234)

        max_num_of_relevant_book = sum(
            rel >= config.RELEVANCE_THRESHOLD
            for rel in ideal_rel_in_order
        )

            # LLM
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

            # RAG
        rag_ndcg = round(normalized_dcg(
            rag_rel_in_order,
            ideal_rel_in_order
        ), config.NUM_DIGITS_ROUNDED_FOR_METRICS)

        rag_precision = round(
            normalized_precision(rag_rel_in_order, config.RELEVANCE_THRESHOLD, max_num_of_relevant_book),
            config.NUM_DIGITS_ROUNDED_FOR_METRICS
        )

        rag_violation_rate = round(
            violation_rate(rag_violation_counter, len(rag_recommeded_books)),
            config.NUM_DIGITS_ROUNDED_FOR_METRICS
        )

            # Baseline
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
                "Baseline_violation_rate": baseline_violation_rate,
                "RAG_ndcg": rag_ndcg,
                "RAG_precision": rag_precision,
                "RAG_violation_rate": rag_violation_rate
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
        print(f"RAG_ndcg: {rag_ndcg}")
        print(f"RAG_precision: {rag_precision}")
        print(f"RAG_violation_rate: {rag_violation_rate}")
        print()
        print()


    # Save eval result
    save_metrics_per_user_to_csv(eval_results)
    save_mean_metrics_to_csv(eval_results)

    # Save what llm and rag actually recommeded for further analysis
    save_books_recommeded_by_llm(all_recommendations_from_llm)
    save_books_recommeded_by_rag(all_recommendations_from_rag)
    save_books_recommeded_by_embedding_model(all_recommendations_from_embedding_model)


if __name__ == "__main__":
    main()