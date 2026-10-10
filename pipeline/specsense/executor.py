# This is a simple executor for the SpecSense AI pipeline. It takes the user product requirements as a message and a strategy as input, 
# and returns the generated prompt based on the strategy.Basically to run the LLM.More like an adapter 
# between the LLM and the pipeline. 

from typing import Optional # Handles Null Objects / optional parameters for the strategy, allowing flexibility in prompt generation.
from llm.client import LLMClient
from utils import get_logger

logger = get_logger(__name__)

class LLMExecutor:
    """
    Executor for the specSense AI recommender Pipeline. It takes a user product requirements message and a strategy as input, 
    and returns the generated prompt based on the strategy.
    """
    def __init__(self, model: Optional[str] = None) -> None:
        """Initialize the LLMExecutor with an optional model name.Take Prompts and pass through the LLM Client."""
        self.llm: LLMClient = LLMClient(model) if model else LLMClient()
        logger.info("LLMExecutor initialized with model %s", self.llm.model_name)

    def execute(self, prompt: str, **kwargs) -> str:
        """
        Execute the prompt using configured LLM client and return the raw response.Acts as an adapter between the underlying LLM implementation and the recommendation pipeline, allowing for easy integration and testing.

        Args: 
            prompt(str):
                The formatted prompt message to send to LLM.
        Returns:
            str:
                The raw text response from LLM. 
        Raises:
            Exception: If the LLM call fails after retries.
        """
        logger.info("Executing prompt with prompt length %d characters", len(prompt))
        try:
            response = self.llm.call(prompt, **kwargs) # LL.CALL Function is called to send the prompt to the LLM and receive the response.
            logger.info("LLM Execution successful. Received response with length: %d characters", len(response))
            return response
        except Exception:
            logger.exception("Error occurred while executing LLM call")
            raise
            