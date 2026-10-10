"""
Minimal Configuration for the SpecSense recommender application.
This file contains the necessary settings and configurations for the
application to be used across different modules."""


import os
from pathlib import Path
from dotenv import load_dotenv

#Path(__file__) is the path of the current file (config.py)
#Path(__file__).parent is parent directory of the current file (config.py)
#Path(__file__).resolve() gives the absolute path of the current file (config.py)

# Load environment variables from .env file
PROJECT_ROOT = Path(__file__).parent
load_dotenv(PROJECT_ROOT / ".env")
# Get the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#LLM Settings
DEFAULT_MODEL = "gemini-2.5-flash"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
#TEMPERATURE SETTINGS CAN ALSO BE ADJUSTED HERE

#PROCESSING SETTINGS
DEFAULT_BATCH_SIZE = 10  # Default batch size for processing
STREAMLIT_BATCH_SIZE = 10  # Batch size for Streamlit processs