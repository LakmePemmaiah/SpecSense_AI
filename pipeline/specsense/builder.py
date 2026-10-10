
from llm.prompts import generate_prompt
from .loader import load_product_catalog, load_user_profiles

def build_prompt(message : str, strategy : str = "react") -> str:
    """
    Build the complete prompt by combining:
    - System Prompt
    - Product Catalog
    - User Profile
    - User Requirement
    """
    product_catalog = load_product_catalog()
    user_profiles = load_user_profiles()

    if strategy == "react":
        return generate_prompt(user_input=message, product_catalog=product_catalog, user_profiles=user_profiles)
    else:
        raise NotImplementedError (f"Strategy: '{strategy}' is not supported. Please choose 'react' for now.")

# To Run this seperately,use python -m pipeline.specsense.builder.
# -m actually asks llm to go from root and search for all the folders 
# at the level of pipeline and check for the modules.At the same time,
# the __init__.py file is important in the folders.