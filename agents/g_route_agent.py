import os
import re
from dotenv import load_dotenv
from .llm_client import get_llm_response

# Load .env
load_dotenv()


def generate_route(plan: dict, draft_html: str):
    print("\n\n⚫ [ROUTE AGENT] Generating Laravel routes...")

    user_prompt = f"""
Based on the following HTML structure and page plan, generate the necessary Laravel route declarations.

📌 Page name: `{plan['page']}`
📌 Route path: `{plan['route']}`

📎 HTML Reference:
```html
{draft_html}
```
Respond ONLY with valid Laravel route definitions using Route::get() in PHP format. Use view() with the correct Blade file name.
"""
    system_prompt = """
You are a Laravel route generation AI.

Given a page name and HTML layout, generate Laravel route declarations in clean PHP format.

Requirements:
- Start with the PHP opening tag `<?php`
- Always include `use Illuminate\\Support\\Facades\\Route;`
- Only use `Route::get()` to return views.
- Do NOT include any explanation or extra text.
- Respond ONLY with the complete PHP code wrapped inside a ```php code block.
"""

    # Use unified LLM client (prioritizes Cerebras, falls back to Mistral)
    try:
        full_response = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=8000,
        )

        # Display response character by character for visual feedback
        for char in full_response:
            print(char, end="", flush=True)

    except Exception as e:
        print(f"\n❌ Failed to generate response: {e}")
        return ""

    match = re.findall(r"```php\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)
    with open("output/web.php", "w", encoding="utf-8") as f:
        f.write(match[0].strip() if match else full_response.strip())
    return match[0].strip() if match else full_response.strip()
    return match[0].strip() if match else full_response.strip()
