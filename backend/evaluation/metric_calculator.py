import math
from collections import Counter


# Metrics for recommenders ---------------------------------------

def dcg(relevance_in_order: list[int]) -> float:

    result = 0.0

    for i, rel in enumerate(relevance_in_order, start=1):
        result += rel / math.log2(i + 1)

    return result


def ideal_dcg(ideal_rel_in_order: list[int]) -> float:

    result = 0.0

    for i, rel in enumerate(ideal_rel_in_order, start=1):
        result += rel / math.log2(i + 1)

    return result


def normalized_dcg(
        relevance_in_order: list[int],
        ideal_rel_in_order: list[int]
) -> float:
    """
    This function checks if the two arguments have equivalent length and
    if ideal_rel_in_order is sorted and contains any numbers rather than
    only zeros. Also, this function expects the two arguments not to be
    empty lists.
    """

    assert len(relevance_in_order) == len(ideal_rel_in_order) != 0, "The length of 'relevance_in_order' must be equal to 'ideal_rel_in_order' and must not be 0"

    is_sorted = True
    last_rel = ideal_rel_in_order[0]
    only_zeros_or_any_negative = True if last_rel <= 0 else False

    for rel in ideal_rel_in_order:

        if rel > last_rel:
            is_sorted = False
            break

        if rel > 0:
            only_zeros_or_any_negative = False
        elif rel < 0:
            only_zeros_or_any_negative = True
            break

        last_rel = rel

    assert is_sorted, "ideal_rel_in_order must be a sorted list[int] from greatest to smallest"

    assert not only_zeros_or_any_negative, "ideal_rel_in_order MUST NOT be a list of ONLY ZEROs or ANY NEGATIVE NUMBERS"

    return dcg(relevance_in_order) / ideal_dcg(ideal_rel_in_order)


def normalized_precision(
        relevance_in_order: list[int],
        rel_threshold: int,
        k: int
) -> float:

    if len(relevance_in_order) == 0:
        return 0.0

    num_of_suitable_book = 0
    for rel in relevance_in_order:
        if rel >= rel_threshold:
            num_of_suitable_book += 1

    return num_of_suitable_book / k


def violation_rate(num_of_violation: int, total_k: int) -> float:

    return num_of_violation / total_k



# Metrics for intent extraction -------------------------------------

def exact_match_accuracy(expected: dict, actual: dict) -> float:
    """1.0 if all entity intents and excluded genres match; otherwise 0.0."""

    expected_entities = Counter(
        (entity["type"], entity["name"], entity["start"], entity["end"], entity["intent"])
        for entity in expected["entities"]
    )
    actual_entities = Counter(
        (entity["type"], entity["name"], entity["start"], entity["end"], entity["intent"])
        for entity in actual["entities"]
    )

    # The order of excluded genres does not matter.
    expected_genres = Counter(expected["excluded_genres"])
    actual_genres = Counter(actual["excluded_genres"])

    return float(expected_entities == actual_entities and expected_genres == actual_genres)


def excluded_genre_precision(expected: dict, actual: dict) -> float | None:
    """Correctly excluded genres / all genres excluded by Qwen."""

    predicted = set(actual["excluded_genres"])
    relevant = set(expected["excluded_genres"])

    if not predicted:
        return None  # Precision is undefined when Qwen predicts no exclusions.

    return len(predicted & relevant) / len(predicted)


def excluded_genre_recall(expected: dict, actual: dict) -> float | None:
    """Correctly excluded genres / all genres that should be excluded."""

    predicted = set(actual["excluded_genres"])
    relevant = set(expected["excluded_genres"])

    if not relevant:
        return None  # Recall is undefined when no genres need excluding.

    return len(predicted & relevant) / len(relevant)


def entity_intent_accuracy(expected: dict, actual: dict) -> float | None:
    """Fraction of ground-truth entity occurrences classified correctly."""

    expected_entities = Counter(
        (entity["type"], entity["name"], entity["start"], entity["end"], entity["intent"])
        for entity in expected["entities"]
    )
    actual_entities = Counter(
        (entity["type"], entity["name"], entity["start"], entity["end"], entity["intent"])
        for entity in actual["entities"]
    )

    total_entities = sum(expected_entities.values())
    if total_entities == 0:
        return None  # Nothing to classify for this user.

    correct_entities = sum((expected_entities & actual_entities).values())
    return correct_entities / total_entities
