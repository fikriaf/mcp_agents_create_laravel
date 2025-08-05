from mistralai import Mistral
import os
from dotenv import load_dotenv

load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

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

    stream = client.chat.stream(
        model="codestral-latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": blade},
        ]
    )

    result = ""
    for chunk in stream:
        content = chunk.data.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            result += content

    return result.strip().upper().startswith("VALID")
