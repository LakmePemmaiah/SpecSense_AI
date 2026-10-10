from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FOLDER = PROJECT_ROOT / "data"

def load_product_catalog() -> pd.DataFrame:
    """Load the product catalog."""
    return pd.read_csv(DATA_FOLDER / "product_catalog.csv")


def load_user_profiles() -> pd.DataFrame:
    """Load the user profiles."""
    return pd.read_csv(DATA_FOLDER / "user_profiles.csv")