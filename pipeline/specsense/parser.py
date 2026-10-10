from typing import Dict, Any, List
from utils import get_logger, extract_json_from_text

logger = get_logger(__name__)


class OutputParser:
    """
    A class to parse the raw output from the LLM and extract
    structured product recommendations.
    """

    def parse_llm_output(self, llm_output: str) -> List[Dict[str, Any]]:
        """
        Parse the LLM output (JSON structure) and extract product
        recommendation entries.

        Supported JSON formats:

        1. Wrapper object (Recommended)
        {
            "recommendations": [
                {...},
                {...},
                {...}
            ]
        }

        2. Backward compatible wrapper
        {
            "products": [
                {...},
                {...}
            ]
        }

        3. JSON Array
        [
            {...},
            {...}
        ]

        4. Single Product Object
        {
            "product_name": "...",
            ...
        }

        Returns:
            List[Dict[str, Any]]

            Always returns a list.
            If parsing fails, returns a list containing a single
            fallback product.
        """

        logger.info(
            f"Parsing LLM output of length {len(llm_output)} characters."
        )

        parsed_json = extract_json_from_text(llm_output)

        # ---------------------------------------------------------
        # Case 1: LLM returned a JSON Array
        # ---------------------------------------------------------
        if isinstance(parsed_json, list):

            recommendations = [
                item for item in parsed_json
                if isinstance(item, dict)
            ]

            if recommendations:
                logger.info(
                    f"Successfully parsed {len(recommendations)} recommendations."
                )
                return recommendations

        # ---------------------------------------------------------
        # Case 2: LLM returned a JSON Object
        # ---------------------------------------------------------
        elif isinstance(parsed_json, dict):

            # Preferred key
            for key in ("recommendations", "products"):

                if isinstance(parsed_json.get(key), list):

                    recommendations = [
                        item
                        for item in parsed_json[key]
                        if isinstance(item, dict)
                    ]

                    if recommendations:
                        logger.info(
                            f"Successfully parsed {len(recommendations)} recommendations."
                        )
                        return recommendations

            # -----------------------------------------------------
            # Case 3: Single recommendation object
            # -----------------------------------------------------

            expected_keys = {
                "product_name",
                "prod_desc",
                "price",
                "rating",
                "hard_matches",
                "soft_matches",
                "trade_offs",
                "Unmet_needs",
            }

            if expected_keys.issubset(parsed_json.keys()):
                logger.info(
                    "Successfully parsed a single product recommendation."
                )
                return [parsed_json]

        # ---------------------------------------------------------
        # Parsing Failed
        # ---------------------------------------------------------

        logger.warning("Failed to parse valid recommendations from LLM output.")

        fallback_result = [
            {
                "product_name": "<No Data Found>",
                "prod_desc": (
                    "Failed to parse the LLM response into the expected "
                    "JSON format."
                ),
                "price": 0.0,
                "rating": 0.0,
                "hard_matches": [],
                "soft_matches": [],
                "trade_offs": [],
                "Unmet_needs": [],
            }
        ]

        return fallback_result