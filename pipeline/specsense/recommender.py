from typing import List, Dict, Any
from .builder import build_prompt
from .executor import LLMExecutor
from .parser import OutputParser
from utils import get_logger

logger = get_logger(__name__)

class SpecSenseRecommender:
    """Orchestrates the specsense AI pipeline"""

    def __init__(self, strategy: str = "react") -> None:
        """Initializes the pipeline components."""
        self.executor = LLMExecutor()
        self.parser = OutputParser()
        self.strategy = strategy
        logger.info(f"Initialized SpecSenseRecommender with strategy: {self.strategy}")

    def recommend(self, message: str) -> List[Dict[str, Any]]:
        """Runs product recommendation on a single message."""
        logger.info(f"Starting recommendation for message length: {len(message)}")
        try:
            # The 3-step pipeline
            prompt = build_prompt(message, self.strategy)
            raw_response = self.executor.execute(prompt)
            parsed_result = self.parser.parse_llm_output(raw_response)

            logger.info(f"Recommendation successful. Returned: {len(parsed_result)} products")
            if parsed_result:
                logger.info(f"Top recommendations: {', '.join([p['product_name'] for p in parsed_result])}")

            return parsed_result

        except Exception:
            # logger.error(f"Recommendation pipeline failed: {e}")
            logger.exception("Recommendation pipeline failed")
            # Re-raise the exception to be handled by the caller (UI layer)
            raise

    def recommend_batch(self, messages: List[str]) -> List[List[Dict[str, Any]]]:
        """Runs product recommendation on a list of messages."""
        total_messages = len(messages)
        logger.info(f"Starting batch recommendation for {total_messages} messages.")
       
        results: List[List[Dict[str, Any]]] = []
       #messages = ["Message 1", "Message 2", "Message 3"]  # Example messages for testing
        for i, message in enumerate(messages):
            try:
                result = self.recommend(message)
                results.append(result)          
            except Exception as e:
                logger.warning(f"Failed to process message {i+1}/{total_messages}: {e}")
                # Append a fallback error result for the failed message
                error_result = {
                    "product_name": "<No Data Found>",
                    "prod_desc": f"Error processing message: {e}",
                    "price": 0.0,
                    "rating": 0.0,
                    "hard_matches": [],
                    "soft_matches": [],
                    "trade_offs": [],
                    "Unmet_needs": []
                }
                results.append([error_result])
       
        successful = sum(
            1
            for r in results 
            if r and r[0]["product_name"] != "<No Data Found>"
            )
        logger.info(f"Batch processing complete. {successful}/{total_messages} succeeded.")
        return results
        #results is a list of dictionaries containing the recommendation results for each message in the input list.        

        # Improvements : define the fallback_product as a constant in config and use it in both recommend and recommend_batch methods to avoid code duplication. (parser & recommender)

