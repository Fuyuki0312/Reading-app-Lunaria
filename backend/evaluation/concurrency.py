from time import perf_counter
import json
import asyncio
from pprint import pprint
from pathlib import Path

from app.config import Config
from app.recommender.rag import recommend_books_with_rag

import pandas as pd


RESULTS_DIR = (
    Path(__file__).resolve().parent
    / "eval_results"
    / "concurrent"
    / "gpt_5_nano"
)


def save_results(
    results: list[dict],
    batch_total_s: float,
    mean_user_latency: float
):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    digits = Config().NUM_DIGITS_ROUNDED_FOR_TIMINGS

    df = pd.DataFrame(results)

    # Save each user's latency
    df.round(digits).to_csv(
        RESULTS_DIR / "per_user_metrics.csv",
        index=False
    )

    # Calculate overall metrics
    summary = {
        "num_users": len(results),
        "batch_total_s": batch_total_s,
        "mean_user_latency_s": mean_user_latency,
        "mean_intent_extraction_s": df["intent_extraction_s"].mean(),
        "mean_embedding_s": df["embedding_s"].mean(),
        "mean_chroma_query_s": df["chroma_query_s"].mean(),
        "mean_llm_rerank_s": df["llm_rerank_s"].mean(),
        "mean_pipeline_total_s": df["pipeline_total_s"].mean()
    }

    pd.DataFrame([summary]).round(digits).to_csv(
        RESULTS_DIR / "mean_metrics.csv",
        index=False
    )

async def benchmark_one_user(user: dict) -> dict:

    timings = {}

    start = perf_counter()

    try:
        await recommend_books_with_rag(
            user_genre_preference=["Fantasy"], # Default genres because there is no fav genres in intent extraction eval dataset
            user_preference_description=user["description"],
            timings=timings
        )

    except Exception as exc:
        print(f"WARNING: user {user['id']} catched an error during concurrency evaluation.")
        print(f"{type(exc).__name__}: {exc}")

    finally:
        timings["user_total_s"] = perf_counter() - start

    return {
        "user_id": user["id"],
        "type": user["type"],
        **timings
    }

async def main():

    dataset_path = (
        Path(__file__).resolve().parent
        / "eval_dataset"
        / "intent_extraction_dataset"
        / "intent_eval_users.json"
    )

    with open(dataset_path, "r", encoding="utf-8") as file:
        users = json.load(file)

    selected_users = users[:10]

    # Warming up recommendation pipeline
    print("Warming up models...")
    await benchmark_one_user(users[0])
    print("Warm-up completed!\n")


    batch_start = perf_counter()

    results = await asyncio.gather(
        *[
            benchmark_one_user(user)
            for user in selected_users
        ]
    )

    batch_total_s = round(perf_counter() - batch_start,
                          Config().NUM_DIGITS_ROUNDED_FOR_TIMINGS)

    # Calculate mean latency for all users
    mean_user_latency = (
        sum(result["user_total_s"] for result in results)
        / len(results)
    )
    mean_user_latency = round(
        mean_user_latency,
        Config().NUM_DIGITS_ROUNDED_FOR_TIMINGS
    )

    # print out latency
    for result in results:
        pprint(result)

    print()
    print(f"Batch total: {batch_total_s}s")
    print(f"Mean user latency: {mean_user_latency}s")


    # save metrics to a csv file
    save_results(
        results=results,
        batch_total_s=batch_total_s,
        mean_user_latency=mean_user_latency
    )


if __name__ == "__main__":
    asyncio.run(main())
