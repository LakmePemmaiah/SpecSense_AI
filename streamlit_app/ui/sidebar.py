"""
sidebar.py

Reusable sidebar component for SpecSense AI.
"""

from typing import Optional
import streamlit as st

from config import DEFAULT_MODEL


def render_sidebar(
    product_count: Optional[int] = None,
    profile_count: Optional[int] = None,
    strategy: str = "ReAct"
) -> None:
    """
    Render the application sidebar.

    Args:
        product_count:
            Number of products loaded from catalog.

        profile_count:
            Number of user profiles loaded.

        strategy:
            Recommendation strategy.
    """

    with st.sidebar:

        # -------------------------------------------------
        # Logo / Title
        # -------------------------------------------------

        st.title("🤖 SpecSense AI")

        st.caption(
            "Bridging User Intent and Product Intelligence"
        )

        st.divider()

        # -------------------------------------------------
        # AI Model Information
        # -------------------------------------------------

        st.subheader("🧠 AI Model")

        st.info(
            f"""
**Model:** {DEFAULT_MODEL}

**Recommendation Strategy:** {strategy}

**Temperature:** 0.2
"""
        )

        st.divider()

        # -------------------------------------------------
        # Data Information
        # -------------------------------------------------

        st.subheader("📂 Dataset")

        if product_count is not None:

            st.success(
                f"✅ Product Catalog Loaded\n\n{product_count:,} Products"
            )

        if profile_count is not None:

            st.success(
                f"✅ Customer Profiles Loaded\n\n{profile_count:,} Profiles"
            )

        st.divider()

        # -------------------------------------------------
        # Recommendation Logic
        # -------------------------------------------------

        st.subheader("⚙️ Ranking Logic")

        st.markdown("""
1. Hard Constraints
2. Soft Preferences
3. Product Rating
4. Price Efficiency
5. Customer Profile
6. Trade-offs
""")

        st.divider()

        # -------------------------------------------------
        # About
        # -------------------------------------------------

        st.subheader("ℹ️ About")

        st.caption(
            """
SpecSense AI recommends products by understanding
natural language requirements and matching them
against structured product specifications.

Recommendations are transparent and explainable,
showing:

- ✅ Hard Matches
- 💡 Soft Matches
- ⚖️ Trade-offs
- ❌ Unmet Needs
- 🎯 Recommendation Confidence
"""
        )

        st.divider()

        st.caption("Developed using Google Gemini & Streamlit")