def calculate_percentage_change(
    old_value: float,
    new_value: float
) -> float:
    """
    Calculate percentage change from old_value to new_value.
    """

    if old_value == 0:
        raise ValueError(
            "Cannot calculate percentage change from zero."
        )

    return ((new_value - old_value) / old_value) * 100


def calculate_difference(
    old_value: float,
    new_value: float
) -> float:
    """
    Calculate the difference between two values.
    """

    return new_value - old_value


def calculate_percentage(
    numerator: float,
    denominator: float
) -> float:
    """
    Calculate numerator as a percentage of denominator.
    """

    if denominator == 0:
        raise ValueError(
            "Cannot divide by zero."
        )

    return (numerator / denominator) * 100