"""
helpers.py

Common helper functions used across the Streamlit UI.
"""

from typing import Any, List


def format_price(price: Any) -> str:
    """
    Format a price value into Indian currency format.

    Examples:
        45999      -> ₹45,999
        "45999"    -> ₹45,999
        "₹45999"   -> ₹45,999
    """

    if price is None:
        return "Not Available"

    try:
        if isinstance(price, str):
            price = (
                price.replace("₹", "")
                .replace(",", "")
                .strip()
            )

        return f"₹{float(price):,.0f}"

    except (ValueError, TypeError):
        return str(price)


def format_rating(rating: Any) -> str:
    """
    Format rating with stars.

    Example:
        4.5 -> ⭐ 4.5 / 5
    """

    if rating is None:
        return "Not Rated"

    try:
        return f"⭐ {float(rating):.1f} / 5"

    except (ValueError, TypeError):
        return "Not Rated"


def get_medal(rank: int) -> str:
    """
    Return medal based on recommendation rank.
    """

    medals = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }

    return medals.get(rank, "⭐")


def ensure_list(value: Any) -> List[str]:
    """
    Ensure the returned value is always a list.

    Examples:
        "Intel i5" -> ["Intel i5"]

        ["Intel i5","16GB RAM"] -> unchanged

        None -> []
    """

    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [str(value)]


def bullet_text(items: List[str]) -> str:
    """
    Convert a list into markdown bullets.

    Example:
        ["Intel i5", "16GB RAM"]

    Returns:

    • Intel i5

    • 16GB RAM
    """

    if not items:
        return "None"

    return "\n".join(f"• {item}" for item in items)


def truncate_text(text: str, max_length: int = 120) -> str:
    """
    Truncate long descriptions for compact UI.
    """

    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."


def confidence_color(confidence: float) -> str:
    """
    Return a color based on confidence score.

    >=90 : Green
    >=75 : Blue
    >=60 : Orange
    <60  : Red
    """

    if confidence >= 90:
        return "green"

    elif confidence >= 75:
        return "blue"

    elif confidence >= 60:
        return "orange"

    return "red"