"""
styles.py

Contains custom CSS styling for SpecSense AI.
"""

import streamlit as st


def load_css() -> None:
    """Load custom CSS for the Streamlit application."""

    st.markdown(
        """
        <style>

        /* -------------------------------
            Main App
        -------------------------------- */

        .main {
            background-color: #F8FAFC;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* -------------------------------
            Sidebar
        -------------------------------- */

        section[data-testid="stSidebar"] {
            background-color: #0F172A;
            color: white;
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }

        /* -------------------------------
            Headers
        -------------------------------- */

        h1 {
            color: #1E3A8A;
            font-weight: 700;
        }

        h2 {
            color: #2563EB;
        }

        h3 {
            color: #334155;
        }

        /* -------------------------------
            Buttons
        -------------------------------- */

        div.stButton > button {
            background-color: #2563EB;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.6rem 1.2rem;
            font-weight: bold;
            transition: 0.3s;
        }

        div.stButton > button:hover {
            background-color: #1D4ED8;
            color: white;
        }

        /* -------------------------------
            Text Area
        -------------------------------- */

        textarea {
            border-radius: 12px !important;
        }

        /* -------------------------------
            Metric Cards
        -------------------------------- */

        div[data-testid="metric-container"] {

            background-color: white;

            border: 1px solid #E2E8F0;

            border-radius: 12px;

            padding: 12px;

            box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
        }

        /* -------------------------------
            Recommendation Cards
        -------------------------------- */

        div[data-testid="stVerticalBlockBorderWrapper"] {

            border-radius: 15px;

            border: 1px solid #CBD5E1;

            padding: 10px;

            background-color: white;

            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);

            margin-bottom: 20px;

        }

        /* -------------------------------
            Expanders
        -------------------------------- */

        details {

            border-radius: 10px;

            border: 1px solid #CBD5E1;

            background-color: #FFFFFF;

        }

        /* -------------------------------
            Progress Bar
        -------------------------------- */

        div[data-testid="stProgressBar"] > div > div {

            background-color: #2563EB;

        }

        /* -------------------------------
            Success Messages
        -------------------------------- */

        div[data-testid="stAlert"] {

            border-radius: 10px;

        }

        /* -------------------------------
            Footer
        -------------------------------- */

        footer {

            visibility: hidden;

        }

        /* -------------------------------
            Streamlit Menu
        -------------------------------- */

        #MainMenu {

            visibility: hidden;

        }

        header {

            visibility: hidden;

        }

        </style>
        """,
        unsafe_allow_html=True,
    )