"""
scoring.py

Business logic for calculating recommendation confidence
based on SpecSense AI ranking strategy.
"""

from typing import Dict, Any


# -----------------------------
# Configurable Weights
# -----------------------------

HARD_MATCH_WEIGHT = 30
SOFT_MATCH_WEIGHT = 30
RATING_WEIGHT = 20
PRICE_WEIGHT = 20
#PROFILE_WEIGHT = 10
#UNMET_PENALTY = 5


# -----------------------------
# Configurable Limits
# -----------------------------

MAX_HARD_MATCHES = 4
MAX_SOFT_MATCHES = 4


def _parse_price(price) -> float:
    """
    Convert price into float.

    Handles:
        ₹45,999
        45999
        "45999"

    Returns:
        float
    """

    if price is None:
        return 0.0

    try:

        if isinstance(price, str):

            price = (
                price.replace("₹", "")
                     .replace(",", "")
                     .strip()
            )

        return float(price)

    except (ValueError, TypeError):

        return 0.0


def calculate_confidence(product: Dict[str, Any]) -> float:
    """
    Calculate recommendation confidence.

    Returns
    -------
    float
        Confidence score between 0 and 100.
    """

    score = 0.0

    # =====================================================
    # 1. Hard Constraint Satisfaction (40)
    # =====================================================

    hard_matches = product.get("hard_matches", [])

    hard_score = (
        min(len(hard_matches), MAX_HARD_MATCHES)
        / MAX_HARD_MATCHES
    ) * HARD_MATCH_WEIGHT

    score += hard_score

    # =====================================================
    # 2. Soft Preference Satisfaction (20)
    # =====================================================

    soft_matches = product.get("soft_matches", [])

    soft_score = (
        min(len(soft_matches), MAX_SOFT_MATCHES)
        / MAX_SOFT_MATCHES
    ) * SOFT_MATCH_WEIGHT

    score += soft_score

    # =====================================================
    # 3. Product Rating (20)
    # =====================================================

    try:

        rating = float(product.get("rating", 0))

        if rating > 4.0:
            score += 20
        elif rating > 3.5:
            score += 15
        elif rating > 3.0:
            score += 10
        else:
            score += 5

        #rating = max(0, min(rating, 5))
        #rating_score = (rating / 5) * RATING_WEIGHT
        #score += rating_score

    except (ValueError, TypeError):

        pass

    # =====================================================
    # 4. Price Efficiency (20)
    # =====================================================

    price = _parse_price(product.get("price"))

    if price > 0:

        if price <= 30000:
            score += 10

        elif price <= 50000:
            score += 9

        elif price <= 75000:
            score += 8

        elif price <= 100000:
            score += 6

        else:
            score += 4

    # =====================================================
    # 5. Customer Profile Alignment (10)
    # =====================================================

    # Placeholder
    #
    # Later you can calculate this based on:
    # - preferred brand
    # - purchase history
    # - category affinity
    # - budget alignment
    #
    # For PoC assume profile is considered.

    #score += PROFILE_WEIGHT

    # =====================================================
    # 6. Penalty for Unmet Needs (-5)
    # =====================================================

    #unmet = product.get("Unmet_needs", [])

    #penalty = min(
    #    len(unmet),
    #    2
    #) * (UNMET_PENALTY / 2)

    #score -= penalty

    # =====================================================
    # Final Score
    # =====================================================

    score = max(0, min(score, 100))

    return round(score, 1)