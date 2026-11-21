from time import perf_counter
import json
import asyncio
from pathlib import Path

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

    user = users[0] # TEST

    result = await benchmark_one_user(user)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
