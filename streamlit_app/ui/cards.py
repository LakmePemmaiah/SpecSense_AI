"""
cards.py

Reusable UI components for displaying product recommendation cards
for SpecSense AI.
"""

from typing import Dict, Any, List
import streamlit as st

from ui.scoring import calculate_confidence


def _render_section(title: str,
                    items: List[str],
                    empty_message: str = "None") -> None:
    """
    Render a list of bullet points.

    Args:
        title: Section title
        items: List of strings
        empty_message: Message when list is empty
    """

    st.markdown(f"#### {title}")

    if items:
        for item in items:
            st.markdown(f"- {item}")
    else:
        st.caption(empty_message)


def render_product_card(product: Dict[str, Any], rank: int) -> None:
    """
    Render a recommendation card.

    Args:
        product:
            Dictionary returned by parser.py

        rank:
            Recommendation rank (1,2,3)
    """

    medal = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }.get(rank, "⭐")

    confidence = calculate_confidence(product)

    with st.container(border=True):

        # ---------------------------------------------------
        # Header
        # ---------------------------------------------------

        col1, col2 = st.columns([5, 1])

        with col1:

            st.markdown(
                f"## {medal} Recommendation #{rank}"
            )

            st.subheader(
                product.get(
                    "product_name",
                    "Unknown Product"
                )
            )

        with col2:

            rating = product.get("rating", "N/A")

            st.metric(
                label="⭐ Rating",
                value=rating
            )

        # ---------------------------------------------------
        # Description
        # ---------------------------------------------------

        st.write(
            product.get(
                "prod_desc",
                "Description not available."
            )
        )

        # ---------------------------------------------------
        # Price
        # ---------------------------------------------------

        price = product.get(
            "price",
            "Not Available"
        )

        st.markdown(
            f"### 💰 Price : **₹ {price}**"
        )

        st.divider()

        # ---------------------------------------------------
        # Confidence
        # ---------------------------------------------------

        st.markdown("### 🎯 Recommendation Confidence")

        st.progress(confidence / 100)

        st.caption(f"Confidence Score : **{confidence:.1f}%**")

        st.divider()

        # ---------------------------------------------------
        # Expanders
        # ---------------------------------------------------

        with st.expander("✅ Hard Matches", expanded=True):

            _render_section(
                "",
                product.get(
                    "hard_matches",
                    []
                ),
                "No hard matches available."
            )

        with st.expander("💡 Soft Matches"):

            _render_section(
                "",
                product.get(
                    "soft_matches",
                    []
                ),
                "No soft matches available."
            )

        with st.expander("⚖ Trade-offs"):

            _render_section(
                "",
                product.get(
                    "trade_offs",
                    []
                ),
                "No trade-offs identified."
            )

        with st.expander("❌ Unmet Needs"):

            _render_section(
                "",
                product.get(
                    "Unmet_needs",
                    []
                ),
                "No unmet needs."
            )


def render_all_cards(
    recommendations: List[Dict[str, Any]]
) -> None:
    """
    Render all recommendation cards.

    Args:
        recommendations:
            List returned by recommender.recommend()
    """

    if not recommendations:

        st.warning(
            "No recommendations found."
        )
        return

    st.subheader("🏆 Top Recommendations")

    for rank, product in enumerate(
        recommendations,
        start=1
    ):

        render_product_card(
            product,
            rank
        )

        st.markdown("<br>", unsafe_allow_html=True)