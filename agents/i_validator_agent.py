from .llm_client import get_llm_response
import os
from dotenv import load_dotenv

load_dotenv()


def validate(blade: str):
    system_prompt = """
You are a Laravel Blade syntax validator.

Your job is to check if a Blade template is structurally correct.

Requirements:
- All sections must be closed properly with @endsection.
- Blade directives like @extends, @include must use correct syntax.
- No missing or unmatched brackets.

If valid, return: VALID.
If invalid, return: INVALID + brief reason.
Only output this result. No code block.
"""

    # Use unified LLM client (prioritizes Cerebras, falls back to Mistral)
    try:
        result = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=blade,
            temperature=0.3,
            max_tokens=8000,
        )

        # Display response character by character for visual feedback
        for char in result:
            print(char, end="", flush=True)

    except Exception as e:
        print(f"❌ Failed to validate: {e}")
        result = "INVALID - Validation service unavailable"

    return result.strip().upper().startswith("VALID")
