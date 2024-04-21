def map_to_range(value: float) -> str:
    """Mapping float values to precipitation conditions range.

    Args:
        value (float): SPI value

    Returns:
        str: Precipitation condition assigned based on range.
    """

    SPI_ranges = {
        "Extremely wet": (2.0, float("inf")),
        "Very wet": (1.5, 1.99),
        "Moderately wet": (1.0, 1.49),
        "Moderate conditions": (-0.99, 0.99),
        "Moderate drought": (-1.49, -1.0),
        "Severe drought": (-1.99, -1.5),
        "Extreme drought": (-float("inf"), -2.0),
    }

    for range_name, (lower_bound, upper_bound) in SPI_ranges.items():
        if lower_bound <= value <= upper_bound:
            return f"{range_name}"
    return "Wrong range"
