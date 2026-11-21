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
        user_genre_preference=["Fantasy"],
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

    selected_users = users[:3]

    await benchmark_one_user(selected_users[0]) # Warming up recommendation pipeline


    batch_start = perf_counter()

    results = await asyncio.gather(
        *[
            benchmark_one_user(user)
            for user in selected_users
        ]
    )

    batch_total_s = round(perf_counter() - batch_start,
                          Config().NUM_DIGITS_ROUNDED_FOR_TIMINGS)

    # print out results
    for result in results:
        pprint(result)

    print(f"Batch total: {batch_total_s}s")


if __name__ == "__main__":
    asyncio.run(main())
