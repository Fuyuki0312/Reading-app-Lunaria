import json
from pathlib import Path

import pandas as pd

from app.config import Config
from app.recommender.rag.llm.intent_extraction import extract_intents
from app.recommender.rag.retrieval.entity_matching import match_entities

from metric_calculator import exact_match_accuracy, excluded_genre_precision, excluded_genre_recall, entity_intent_accuracy

# Paths ---------------------------------------------------------

EVALUATION_DIR = Path(__file__).resolve().parent

DATASET_DIR = EVALUATION_DIR / "eval_dataset" / "intent_extraction_dataset"
USER_DATASET_PATH = DATASET_DIR / "intent_eval_users.json"
GROUND_TRUTH_PATH = DATASET_DIR / "intent_eval_ground_truth.json"

RESULTS_DIR = EVALUATION_DIR / "eval_results" / "intent_extraction_metrics"
PER_USER_METRICS_PATH = RESULTS_DIR / "per_user_metrics.csv"
MEAN_METRICS_BY_TYPE_PATH = RESULTS_DIR / "mean_metrics_by_type.csv"
OVERALL_METRICS_PATH = RESULTS_DIR / "mean_metrics.csv"
QWEN_OUTPUTS_PATH = RESULTS_DIR / "analysis" / "qwen_outputs.json"

METRIC_COLUMNS = [
    "exact_match_accuracy",
    "excluded_genre_precision",
    "excluded_genre_recall",
    "entity_intent_accuracy"
]

config = Config()


# Save functions -------------------------------------------------

def save_results(metrics_per_user: list[dict], qwen_outputs: list[dict]):
    """Save all four metrics and the raw extraction outputs after each user."""

    df = pd.DataFrame(metrics_per_user)
    df[METRIC_COLUMNS] = df[METRIC_COLUMNS].apply(pd.to_numeric, errors="coerce")

    digits = config.NUM_DIGITS_ROUNDED_FOR_METRICS

    df.round(digits).to_csv(PER_USER_METRICS_PATH, index=False)

    # pandas.mean() ignores None/NaN. A missing metric is not treated as 0 or 1.
    mean_by_type = df.groupby("type", sort=False)[METRIC_COLUMNS].mean()
    mean_by_type.round(digits).to_csv(MEAN_METRICS_BY_TYPE_PATH)

    overall_mean = df[METRIC_COLUMNS].mean().round(digits)
    pd.DataFrame([overall_mean.to_dict()]).to_csv(OVERALL_METRICS_PATH, index=False)

    with open(QWEN_OUTPUTS_PATH, "w", encoding="utf-8") as file:
        json.dump(qwen_outputs, file, ensure_ascii=False, indent=4)


def format_metric(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.4f}"


# Evaluation -----------------------------------------------------

def main():
    with open(USER_DATASET_PATH, "r", encoding="utf-8") as file:
        eval_users = json.load(file)

    with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as file:
        eval_ground_truth = json.load(file)

    # Pair records by ID, not by their position inside the JSON lists.
    user_ids = [user["id"] for user in eval_users]
    truth_ids = [item["id"] for item in eval_ground_truth]

    if not eval_users:
        raise ValueError("The user evaluation dataset is empty.")
    if len(set(user_ids)) != len(user_ids) or len(set(truth_ids)) != len(truth_ids):
        raise ValueError("Duplicated IDs in the evaluation dataset.")
    if set(user_ids) != set(truth_ids):
        raise ValueError("User IDs and ground-truth IDs do not match.")

    ground_truth_by_id = {
        item["id"]: item["expected_output"]
        for item in eval_ground_truth
    }

    QWEN_OUTPUTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    metrics_per_user = []
    qwen_outputs = []

    for user in eval_users:
        user_id = user["id"]
        description = user["description"]
        expected = ground_truth_by_id[user_id]

        print(f"Evaluating Qwen for user {user_id} ({user['type']})...")

        matched_entities = match_entities(description)
        actual = extract_intents(
            user_description=description,
            entities=matched_entities
        )

        metrics = {
            "user_id": user_id,
            "type": user["type"],
            "exact_match_accuracy": exact_match_accuracy(expected, actual),
            "excluded_genre_precision": excluded_genre_precision(expected, actual),
            "excluded_genre_recall": excluded_genre_recall(expected, actual),
            "entity_intent_accuracy": entity_intent_accuracy(expected, actual)
        }
        metrics_per_user.append(metrics)

        qwen_outputs.append({
            "user_id": user_id,
            "type": user["type"],
            "description": description,
            "matched_entities": matched_entities,
            "qwen_output": actual
        })

        for metric_name in METRIC_COLUMNS:
            print(f"{metric_name}: {format_metric(metrics[metric_name])}")
        print()

        # Preserve finished users' results if a later Ollama request fails.
        save_results(metrics_per_user, qwen_outputs)

    print(f"Evaluation finished. Results saved to: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
