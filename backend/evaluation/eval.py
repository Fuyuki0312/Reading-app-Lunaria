from baseline import Baseline #.
from app.ai.recommendation import recommend_books

import json


# Get dataset -----------------------------------------------


with open("eval_dataset\\eval_users.json") as f:
    eval_users = json.load(f)

# Baseline initialization -----------------------------------

baseline = Baseline()

# LLM recommending books ------------------------------------

for user in eval_users:

    baseline_recommended_books = baseline.score_books(
        user_genre_preferences=user["genre_preferences"]
    )

    llm_recommeded_books = recommend_books(
        user_genre_preference=user["genre_preferences"],
        user_preference_description=user["genre_description"]
    )