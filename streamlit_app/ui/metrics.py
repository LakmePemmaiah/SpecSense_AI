"""
metrics.py

Reusable summary metrics for SpecSense AI.
"""

from typing import List, Dict, Any
import streamlit as st

from ui.scoring import calculate_confidence


def _parse_price(price) -> float:
    """
    Convert price to float.

    Handles values like:
        ₹45,999
        45999
        "45999"

    Returns 0 if parsing fails.
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


def render_metrics(recommendations: List[Dict[str, Any]]) -> None:
    """
    Display summary metrics for all recommendations.

    Args:
        recommendations:
            Output returned from recommender.recommend()
    """

    if not recommendations:
        st.warning("No recommendations available.")
        return

    total_products = len(recommendations)

    ratings = []
    prices = []
    confidence_scores = []

    total_hard_matches = 0
    total_soft_matches = 0

    for product in recommendations:

        # -----------------------------
        # Rating
        # -----------------------------

        try:
            ratings.append(float(product.get("rating", 0)))
        except (ValueError, TypeError):
            pass

        # -----------------------------
        # Price
        # -----------------------------

        prices.append(_parse_price(product.get("price")))

        # -----------------------------
        # Confidence
        # -----------------------------

        confidence_scores.append(
            calculate_confidence(product)
        )

        # -----------------------------
        # Hard Matches
        # -----------------------------

        total_hard_matches += len(
            product.get("hard_matches", [])
        )

        # -----------------------------
        # Soft Matches
        # -----------------------------

        total_soft_matches += len(
            product.get("soft_matches", [])
        )

    # --------------------------------------
    # Aggregate Metrics
    # --------------------------------------

    avg_rating = (
        round(sum(ratings) / len(ratings), 2)
        if ratings else 0
    )

    avg_price = (
        round(sum(prices) / len(prices), 2)
        if prices else 0
    )

    avg_confidence = (
        round(sum(confidence_scores) / len(confidence_scores), 1)
        if confidence_scores else 0
    )

    # --------------------------------------
    # Display
    # --------------------------------------

    st.subheader("📊 Recommendation Summary")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "📦 Products",
            total_products
        )

    with col2:
        st.metric(
            "⭐ Avg Rating",
            avg_rating
        )

    with col3:
        st.metric(
            "💰 Avg Price",
            f"₹{avg_price:,.0f}"
        )

    with col4:
        st.metric(
            "🎯 Avg Confidence",
            f"{avg_confidence}%"
        )

    with col5:
        st.metric(
            "✅ Hard Matches",
            total_hard_matches
        )

    st.caption(
        f"💡 Total Soft Matches Identified: **{total_soft_matches}**"
    )