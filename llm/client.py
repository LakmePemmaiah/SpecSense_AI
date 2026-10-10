""""LLM Client with Google Gemini API Key along with retry Logic and Error Handling."""
#Authentication : API keys and security
#Rate Limiting : API usage quotas and delay
#Network issues : Transient network failures and timeouts
#Response validation : Ensuring valid responses
#Communication layer 
#Exponential backoff : Increasing delay between retries.
import time
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, DEFAULT_MODEL, MAX_RETRIES, RETRY_DELAY
from utils import get_logger

logger = get_logger(__name__)

#No Execution happening, when executor(communication that happens with API , LLM) runs ,
#  How do you want to handle the errors and retries? Do you want to raise an exception
#  or return a default response?


class LLMClient:
    """Gemini API client"""
    #__init__ function below initializes the LLMClient with model name, max retries, and retry delay.
    #  It also creates a Gemini API client using the provided API key.self is a reference to the 
    # instance of the class, allowing access to its attributes and methods. This is basically 
    # showing the class all the attributes that we have configured earlier.(Basically, init constructutor
    # is showing the class how class is supposed to be used and not calling the LLM API yet.)
    def __init__(self, model_name: str = DEFAULT_MODEL, max_retries: int = MAX_RETRIES, retry_delay: int = RETRY_DELAY):
        self.model_name = model_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
    # **kwargs allows you to pass a variable number of keyword arguments to the function later.more args can be added based on user needs
    def call(self, prompt: str, **kwargs) -> str:
        """Send prompt to Gemini API"""
        for attempt in range(self.max_retries + 1):
            try:
                config = kwargs.pop(
                    "config",
                    types.GenerateContentConfig(temperature=0.2)
                    )
                response = self.client.models.generate_content(
                    contents=prompt, 
                    model=self.model_name, 
                    config = config,
                    **kwargs
                )
                if response and response.text:
                    return response.text.strip()
                else:
                    raise RuntimeError("Gemini returned empty response.")
                
            except Exception as e:
                if attempt == self.max_retries:
                    raise RuntimeError(f"API call failed after {self.max_retries + 1} attempts: {e}")

                delay = self.retry_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)