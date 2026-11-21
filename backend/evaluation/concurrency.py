from time import perf_counter
import json
import asyncio
from pprint import pprint
from pathlib import Path

from app.config import Config
from app.recommender.rag import recommend_books_with_rag


async def benchmark_one_user(user: dict) -> dict:

    timings = {}

    start = perf_counter()

    await recommend_books_with_rag(
        user_genre_preference=["Fantasy"], # Default genres because there is no fav genres in intent extraction eval dataset
        user_preference_description=user["description"],
        timings=timings
    )

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
    print(f"Mean user latency: {mean_user_latency:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())
