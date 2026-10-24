from app.recommender.baseline.baseline import Baseline
from app.recommender.rag.rag_recommendation import recommend_books_with_rag
from app.services.book_services import get_book_services
from metric_calculator import normalized_dcg, normalized_precision, violation_rate
from app.recommender.rag.llm.llm_recommendation import recommend_books_with_llm
from app.config import Config

import torch
import json
import pandas as pd
import time

from pathlib import Path


# Priority bias and model name
# ⚠️: Look at these 2 below Hyperparameters before run this file

PRIORITY_BIAS = "text_description_priority" # "genre_match_priority" or "text_description_priority"
MODEL_NAME_FOR_PATH = "gpt_5_nano" # take a look at app/config.py


# Hyperparameters (where to save) -------------------------------

priority_bias_plus_relevance = PRIORITY_BIAS + "_relevance"

USER_DATASET_PATH = Path("eval_dataset") / "eval_users.json"
BOOK_DATASET_PATH = Path("eval_dataset") / priority_bias_plus_relevance / "relevance_labels.json"

PER_USER_METRICS_PATH = Path("eval_results") / PRIORITY_BIAS / MODEL_NAME_FOR_PATH / "per_user_metrics.csv"
OVERALL_METRICS_PATH = Path("eval_results") / PRIORITY_BIAS / MODEL_NAME_FOR_PATH / "mean_metrics.csv"

BOOK_DETAILS_BY_LLM_PATH = Path("eval_results") / PRIORITY_BIAS / MODEL_NAME_FOR_PATH / "analysis" / "books_from_llm.json"
BOOK_DETAILS_BY_RAG_PATH = Path("eval_results") / PRIORITY_BIAS / MODEL_NAME_FOR_PATH / "analysis" / "books_from_rag.json"


# Config and services --------------------------------------------

config = Config()
book_services = get_book_services()
torch.manual_seed(config.TORCH_SEED)


# Save functions

def save_metrics_per_user_to_csv(one_user_metric_results: list[dict]):
    df = pd.DataFrame(one_user_metric_results)
    df.to_csv(
        PER_USER_METRICS_PATH,
        index=False
    )


def save_mean_metrics_to_csv(one_user_metric_results: list[dict]):

    df = pd.DataFrame(one_user_metric_results).drop(columns=["user_id"])
    mean_metrics = df.mean()

    mean_metrics.index = [f"{metric}_mean" for metric in mean_metrics.index]
    mean_metrics.to_frame().T.to_csv(
        OVERALL_METRICS_PATH,
        index=False
    )


def save_books_recommeded_by_llm(recommendations_from_llm):

    with open(BOOK_DETAILS_BY_LLM_PATH, "w") as file:
        json.dump(recommendations_from_llm, file, indent=4)


def save_books_recommeded_by_rag(recommendations_from_rag):

    with open(BOOK_DETAILS_BY_RAG_PATH, "w") as file:
        json.dump(recommendations_from_rag, file, indent=4)


# Get dataset -----------------------------------------------


with open(USER_DATASET_PATH, "r") as f:
    eval_users = json.load(f)

with open(BOOK_DATASET_PATH, "r") as f:
    eval_relevance = json.load(f)


# Baseline initialization -----------------------------------

baseline = Baseline()

# Warm-up LLM's API -----------------------------------------

temp = recommend_books_with_llm(
    user_genre_preference=["Fantasy", "Adventure"],
    user_preference_description="I love Magical World",
    books=book_services.get_books_with_genres()
)

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

def main():

    for user in eval_users:

        # Get ideal recommendations

        user_id = user["id"]
        ideal_recommended_books_in_order = []

        relevance_start_idx = number_of_books * (user_id - 1)
        relevance_end_idx = relevance_start_idx + number_of_books

        assert type(relevance_start_idx) is int, "relevance_start_idx is NOT int, check relevance_start_idx's equation"
        assert type(relevance_end_idx) is int, "relevance_end_idx is NOT int, check relevance_end_idx's equation"

        book_id_with_relevance_score: dict[int, dict] = {}  # = { int: {"rel_score": rel_score,
                                                            #           "violation": bool} }
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


        print(f"Recommending books for user {user['id']}...\n")

        # Get recommendations from baseline

        start_time = time.perf_counter()
        baseline_recommended_books = baseline.score_books(
            user_genre_preferences=user["genre_preferences"]
        )
        baseline_latency = time.perf_counter() - start_time

        # Get recommendations from LLM

        start_time = time.perf_counter()
        llm_recommeded_books = recommend_books_with_llm(
            user_genre_preference=user["genre_preferences"],
            user_preference_description=user["genre_description"],
            books=book_services.get_books_with_genres()
        )
        llm_latency = time.perf_counter() - start_time

        # The below assertions do 3 things:
        # 1. Check if LLM recommended exactly (config.NUM_OF_RECOMMENDED_BOOK) books
        # 2. Check if recommended books are duplicated
        # 3. Check if all recommeneded books exist in database
        assert len(llm_recommeded_books) == config.NUM_OF_RECOMMENDED_BOOK, (f"LLM did not recommend exactly {config.NUM_OF_RECOMMENDED_BOOK} books for user with id {user['id']}:\n\n"
                                                                             f"{llm_recommeded_books}")
        ids_temp = [book.book_id for book in llm_recommeded_books]

        assert len(ids_temp) == len(set(ids_temp)), (f"Books recommended by the LLM is duplicated:\n\n"
                                                     f"{llm_recommeded_books}")
        assert all(book_id in book_id_with_relevance_score for book_id in ids_temp), (
            f"Books recommended by the LLM do not exist in database:\n\n"
            f"{llm_recommeded_books}"
        )

        all_recommendations_from_llm.append(
            {
                "user_id": user["id"],
                "recommendations": [
                    book.model_dump()
                    for book in llm_recommeded_books
                ]
            }
        )

        # Get recommendations from RAG

        start_time = time.perf_counter()
        rag_recommeded_books = recommend_books_with_rag(
            user_genre_preference=user["genre_preferences"],
            user_preference_description=user["genre_description"]
        )
        rag_latency = time.perf_counter() - start_time

        assert len(rag_recommeded_books) == config.NUM_OF_RECOMMENDED_BOOK, (f"RAG did not recommend exactly {config.NUM_OF_RECOMMENDED_BOOK} books for user with id {user['id']}:\n\n"
                                                                             f"{rag_recommeded_books}")
        ids_temp = [book.book_id for book in rag_recommeded_books]

        assert len(ids_temp) == len(set(ids_temp)), (f"Books recommended by RAG is duplicated:\n\n"
                                                     f"{rag_recommeded_books}")
        assert all(book_id in book_id_with_relevance_score for book_id in ids_temp), (
            f"Books recommended by RAG do not exist in database:\n\n"
            f"{rag_recommeded_books}"
        )

        all_recommendations_from_rag.append(
            {
                "user_id": user["id"],
                "recommendations": [
                    book.model_dump()
                    for book in rag_recommeded_books
                ]
            }
        )


        # Get relevance score and violation rate from each method's recommendations

            # Ideal
        ideal_rel_in_order = []
        for book_rel in ideal_recommended_books_in_order:
            ideal_rel_in_order.append(book_rel["relevance"])

            # LLM only
        llm_rel_in_order = []
        llm_violaion_counter = 0
        for book in llm_recommeded_books:
            book_id = book.book_id
            rel = book_id_with_relevance_score[book_id]["rel_score"]

            if book_id_with_relevance_score[book_id]["violation"]:
                llm_violaion_counter += 1

            llm_rel_in_order.append(rel)

            # RAG
        rag_rel_in_order = []
        rag_violation_counter = 0
        for book in rag_recommeded_books:
            book_id = book.book_id
            rel = book_id_with_relevance_score[book_id]["rel_score"]

            if book_id_with_relevance_score[book_id]["violation"]:
                rag_violation_counter += 1

            rag_rel_in_order.append(rel)


            # Baseline
        baseline_rel_in_order = []
        baseline_violation_counter = 0
        for book in baseline_recommended_books:
            book_id = book.book_id
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
                "LLM_latency": llm_latency,
                "Baseline_ndcg": baseline_ndcg,
                "Baseline_precision": baseline_precision,
                "Baseline_violation_rate": baseline_violation_rate,
                "Baseline_latency": baseline_latency,
                "RAG_ndcg": rag_ndcg,
                "RAG_precision": rag_precision,
                "RAG_violation_rate": rag_violation_rate,
                "RAG_latency": rag_latency
            }
        )

        print(f"LLM_ndcg: {llm_ndcg}")
        print(f"LLM_precision: {llm_precision}")
        print(f"LLM_violation_rate: {llm_violation_rate}")
        print(f"LLM_latency: {llm_latency:.4f} s/user")
        print()
        print(f"Baseline_ndcg: {baseline_ndcg}")
        print(f"Baseline_precision: {baseline_precision}")
        print(f"Baseline_violation_rate: {baseline_violation_rate}")
        print(f"Baseline_latency: {baseline_latency:.4f} s/user")
        print()
        print(f"RAG_ndcg: {rag_ndcg}")
        print(f"RAG_precision: {rag_precision}")
        print(f"RAG_violation_rate: {rag_violation_rate}")
        print(f"RAG_latency: {rag_latency:.4f} s/user")
        print()
        print()


    # Save eval result
    save_metrics_per_user_to_csv(eval_results)
    save_mean_metrics_to_csv(eval_results)

    # Save what llm and rag actually recommeded for further analysis
    save_books_recommeded_by_llm(all_recommendations_from_llm)
    save_books_recommeded_by_rag(all_recommendations_from_rag)


if __name__ == "__main__":
    main()