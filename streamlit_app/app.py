"""
app.py

Main Streamlit application for SpecSense AI.
"""

import streamlit as st
import pandas as pd

from pathlib import Path
import sys

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from pipeline.specsense.recommender import SpecSenseRecommender

from ui.styles import load_css
from ui.sidebar import render_sidebar
from ui.metrics import render_metrics
from ui.cards import render_all_cards

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="SpecSense AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

@st.cache_data
def load_product_catalog():
    return pd.read_csv(PROJECT_ROOT / "data" / "product_catalog.csv")


@st.cache_data
def load_user_profiles():
    return pd.read_csv(PROJECT_ROOT / "data" / "user_profiles.csv")


product_catalog = load_product_catalog()
user_profiles = load_user_profiles()

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

render_sidebar(
    product_count=len(product_catalog),
    profile_count=len(user_profiles),
    strategy="ReAct"
)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🤖 SpecSense AI")

st.caption(
    "Bridging User Intent and Product Intelligence"
)

st.divider()

# ---------------------------------------------------------
# User Input
# ---------------------------------------------------------

user_requirement = st.text_area(
    label="Describe your product requirements",
    placeholder="""
Example:
Looking for a lightweight laptop under ₹60,000 with
16GB RAM, Intel i5 processor, good battery life,
and suitable for coding.
""",
    height=180,
)

recommend_button = st.button(
    "🔍 Recommend Products",
    use_container_width=True
)

# ---------------------------------------------------------
# Recommendation
# ---------------------------------------------------------

if recommend_button:

    if not user_requirement.strip():

        st.warning(
            "Please enter your product requirements."
        )

        st.stop()

    recommender = SpecSenseRecommender()

    with st.spinner("Finding the best products for you..."):

        try:

            recommendations = recommender.recommend(
                user_requirement
            )

            st.success(
                f"Found {len(recommendations)} recommendation(s)."
            )

            st.divider()

            # -------------------------------------
            # Summary Metrics
            # -------------------------------------

            render_metrics(recommendations)

            st.divider()

            # -------------------------------------
            # Product Cards
            # -------------------------------------

            render_all_cards(recommendations)

        except Exception as e:

            st.error("Recommendation failed.")

            st.exception(e)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "SpecSense AI • Powered by Google Gemini • Built with Streamlit"
)