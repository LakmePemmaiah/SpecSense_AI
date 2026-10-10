# llm/prompts.py
from pathlib import Path
#Below is not required when Utils is created as a folder and __init__.py is created inside it. 
# Then we can import utils directly. ex: Utils--> __init__.py,helper.py function having utils.py contents.

#import sys
#sys.path.append(str(Path(__file__).parent.parent))

import json
import pandas as pd

from utils import load_file
# Directory paths
PROMPTS_DIR = Path(__file__).parent / "prompts"
#print(PROMPTS_DIR)
# Load prompt templates from external files
def load_prompt(filename: str) -> str:
    """Load a prompt template from file."""
    return load_file(PROMPTS_DIR / filename)

# Available prompt templates
PROMPT = load_prompt("react.md") # <-- Edit this to use different prompts
#print(PROMPT)

def generate_prompt(user_input: str, product_catalog: pd.DataFrame, user_profiles: pd.DataFrame) -> str:
    """
    Generate a prompt for specSense AI - choose your strategy here!
        
    Args:
        user_input: ThE user-provided message or requirements for product recommendation.
        product_catalog: DataFrame containing the product catalog.
        user_profiles: DataFrame containing the user profiles.
              
    Returns:
        A formatted prompt string ready for LLM execution
    """
    product_catalog_json = product_catalog.to_dict(orient="records")
    user_profiles_json = user_profiles.to_dict(orient="records")

    template = PROMPT
    return f"""{template}\n\n
    You are provided with two datasets.
    Dataset 1: Product Catalog
    Dataset 2: Customer Profiles

    Rules:
    1. Recommend ONLY products that exist in Product Catalog.
    2. Never invent specifications.
    3. Never modify prices.
    4. Use Customer Profile only if relevant.
    5. If information is unavailable, return "Not available in product catalog."

    Product Catalog:
    {json.dumps(product_catalog_json, indent=2)}

    Customer Profiles:
    {json.dumps(user_profiles_json, indent=2)}

    User Requirement:
    {user_input.strip()}

    Return ONLY valid JSON.
    """