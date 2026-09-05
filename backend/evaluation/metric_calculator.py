import math

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