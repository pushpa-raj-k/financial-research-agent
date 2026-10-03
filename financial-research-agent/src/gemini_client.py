import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)


def generate_content(
    prompt: str,
    max_retries: int = 3
):
    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=prompt
            )

        except Exception as e:
            error_text = str(e)

            temporary_error = any(
                code in error_text
                for code in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED"
                ]
            )

            if not temporary_error:
                raise

            if attempt == max_retries - 1:
                raise

            wait_time = 2 ** attempt
            time.sleep(wait_time)
