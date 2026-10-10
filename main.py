# main.py

from pathlib import Path
import sys
# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from pipeline.specsense.recommender import SpecSenseRecommender
from utils import get_logger

logger = get_logger(__name__)

def main():
    """Recommend products based on dynamic user requirements."""
    recommender = SpecSenseRecommender()
    
    user_requirement = input("Enter your Product Requirements: ").strip()
    
    try:
        logger.info("Running product recommendation")
        recommendations = recommender.recommend(user_requirement)
        
        print(f"\nUser Requirement: \n{user_requirement}\n")
        print("Top Recommendations:\n")
        for i, product in enumerate(recommendations, start=1):
            print(f"Recommendation {i}")
            print(f"   Product Name: {product['product_name']}")
            print(f"   Description: {product['prod_desc']}")
            print(f"   Price: {product['price']}")
            print(f"   Rating: {product['rating']}")
            print(f"   Hard Matches: {product['hard_matches']}")
            print(f"   Soft Matches: {product['soft_matches']}\n")
            print(f"   Trade-offs: {product['trade_offs']}")
            print(f"   Unmet Needs: {product['Unmet_needs']}")
            print("-" * 60)
       # print(f"Recommended Result: {result}")
        
    except Exception as e:
        logger.exception("Recommendation failed")
        print("\nAn unexpected error occurred while processing your request. Please try again later.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()