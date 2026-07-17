import os
import time
from google import genai
import logging

logger = logging.getLogger("engipilot")

_client = None

# Ordered by preference — code tries each until one works.
# If Google deprecates one, the next in line takes over automatically.
MODEL_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-latest",
]


def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


def generate_text(prompt: str, max_retries_per_model: int = 2) -> str:
    """
    Generates text using Gemini, automatically falling back across multiple
    model candidates if one is deprecated (404) or over quota (429/503).
    Raises the last error if all candidates fail.
    """
    client = _get_client()
    last_error = None

    for model_name in MODEL_CANDIDATES:
        for attempt in range(max_retries_per_model):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                logger.info(f"Gemini call succeeded using model={model_name}")
                return response.text.strip()

            except Exception as e:
                err_str = str(e)
                last_error = e

                if "404" in err_str or "NOT_FOUND" in err_str:
                    # This model is gone — don't retry it, move to the next candidate
                    logger.info(f"Model {model_name} unavailable (404), trying next candidate")
                    break

                if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                    logger.info(f"Model {model_name} overloaded/quota-limited, retry {attempt + 1}/{max_retries_per_model}")
                    time.sleep(2 * (attempt + 1))
                    continue

                # Unknown error — don't keep retrying this model, move on
                logger.info(f"Model {model_name} failed with unexpected error: {e}")
                break

    raise Exception(f"All Gemini model candidates failed. Last error: {last_error}")